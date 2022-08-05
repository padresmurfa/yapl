use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::module_parser::TranspilerFrontendModuleParser;
use crate::transpiler_frontend::parsers::prefix_comment_parser::TranspilerFrontendPrefixCommentParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};

#[derive(Debug, Clone)]
pub struct TranspilerFrontendFileParser {
    // this is currently a constant, 0, but I'm keeping it in a variable for consistency with other parsers and for a hypothetical future case
    // where we use this parser for embedded text and erroneous text, which doesn't necessarily start at indentation 0
    internal_indentation_level: usize
}

enum TranspilerFrontendFileParserLineClassification {
    Comment,
    ModuleStatement,
    IndentedLine,
    JunkLine,
    EmptyLine
}

impl TranspilerFrontendParser for TranspilerFrontendFileParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::FileParser;
    }

    fn as_file_parser(&self) -> Option<&TranspilerFrontendFileParser> {
        return Some(&self);
    }
    
}

impl TranspilerFrontendFileParser {

    pub fn create() -> Box<TranspilerFrontendFileParser> {
        return Box::new(TranspilerFrontendFileParser {
            internal_indentation_level: 0
        });
    }

    fn classify_line(&self, text: &String) -> TranspilerFrontendFileParserLineClassification {
        let trimmed = text.trim_start();
        if trimmed.is_empty() {
            return TranspilerFrontendFileParserLineClassification::EmptyLine;
        } else if trimmed == text {
            if trimmed.starts_with("module ") {
                return TranspilerFrontendFileParserLineClassification::ModuleStatement;
            } else if trimmed.starts_with("--") {
                return TranspilerFrontendFileParserLineClassification::Comment;
            } else {
                return TranspilerFrontendFileParserLineClassification::JunkLine;
            }
        } else {
            return TranspilerFrontendFileParserLineClassification::IndentedLine;
        }
    }
    
    fn on_module_statement_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let parser = TranspilerFrontendModuleParser::create(self.internal_indentation_level, context, line);
        context.request_push(parser);
    }

    fn on_comment_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let parser = TranspilerFrontendPrefixCommentParser::create(self.internal_indentation_level, context, line);
        context.request_push(parser);
    }

    fn on_error_indented_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected indented line encountered in file scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendFileParserInvalidIdentedLine,
            line
        );
    }

    fn on_error_junk_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected initial token encountered in file scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendFileParserInvalidStartingToken,
            line
        );
    }

    fn on_empty_line(&mut self, _context: &mut TranspilerFrontendContext, _line: &TranspilerFrontendLine) {
        // TODO - transform prefix comment into infix comment, if present on the stack
    }
}

impl TranspilerFrontend for TranspilerFrontendFileParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let classification = self.classify_line(&line.line_text);
        match classification {
            TranspilerFrontendFileParserLineClassification::ModuleStatement => {
                self.on_module_statement_line(context, &line);
            }
            TranspilerFrontendFileParserLineClassification::Comment => {
                self.on_comment_line(context, &line);
            }
            TranspilerFrontendFileParserLineClassification::IndentedLine => {
                self.on_error_indented_line(context, &line);
            }
            TranspilerFrontendFileParserLineClassification::JunkLine => {
                self.on_error_junk_line(context, &line);
            }
            TranspilerFrontendFileParserLineClassification::EmptyLine => {
                self.on_empty_line(context, &line);
            }
        }
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        context.request_pop_due_to_end_of_file();
    }
}
