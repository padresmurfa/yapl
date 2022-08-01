use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
//use crate::transpiler_frontend::parsers::class_parser::TranspilerFrontendClassParser;
//use crate::transpiler_frontend::parsers::function_parser::TranspilerFrontendFunctionParser;
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
pub struct TranspilerFrontendModuleParser {
    external_indentation_level: usize,
    internal_indentation_level: usize
}

enum TranspilerFrontendModuleParserLineClassification {
    Comment,
    ClassStatement,
    FunctionStatement,
    IndentedLine,
    JunkLine,
    EmptyLine
}

impl TranspilerFrontendParser for TranspilerFrontendModuleParser {
    fn get_parser_type_identifier() -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::ModuleParser;
    }

    fn as_module_parser(&self) -> Option<&TranspilerFrontendModuleParser> {
        return Some(&self);
    }
    
}

impl TranspilerFrontendModuleParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<dyn TranspilerFrontend> {
        let mut result = Box::new(TranspilerFrontendModuleParser {
            external_indentation_level: external_indentation_level,
            internal_indentation_level: external_indentation_level
        });
        result.append_line(context, line);
        return result;
    }

    fn classify_line(&self, text: &String) -> TranspilerFrontendModuleParserLineClassification {
        let trimmed = text.trim_start();
        if trimmed.is_empty() {
            return TranspilerFrontendModuleParserLineClassification::EmptyLine;
        } else if trimmed == text {
            if trimmed.starts_with("class ") {
                return TranspilerFrontendModuleParserLineClassification::ClassStatement;
            } else if trimmed.starts_with("function ") {
                return TranspilerFrontendModuleParserLineClassification::ClassStatement;
            } else if trimmed.starts_with("--") {
                return TranspilerFrontendModuleParserLineClassification::Comment;
            } else {
                return TranspilerFrontendModuleParserLineClassification::JunkLine;
            }
        } else {
            return TranspilerFrontendModuleParserLineClassification::IndentedLine;
        }
    }
    
    fn on_class_statement_line(&mut self, contxt: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        // let parser = TranspilerFrontendClassParser::create(self.internal_indentation_level, context, line);
        // context.request_push(parser);
    }

    fn on_function_statement_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        // let parser = TranspilerFrontendFunctionParser::create(self.internal_indentation_level, context, line);
        // context.request_push(parser);
    }

    fn on_comment_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let parser = TranspilerFrontendPrefixCommentParser::create(self.internal_indentation_level, context, line);
        context.request_push(parser);
    }

    fn on_error_indented_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected indented line encountered in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserInvalidIdentedLine,
            line
        );
    }

    fn on_error_junk_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected initial token encountered in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserInvalidStartingToken,
            line
        );
    }

    fn on_empty_line(&mut self, _context: &mut TranspilerFrontendContext, _line: &TranspilerFrontendLine) {
        // TODO - transform prefix comment into infix comment, if present on the stack
    }
}

impl TranspilerFrontend for TranspilerFrontendModuleParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let classification = self.classify_line(&line.line_text);
        match classification {
            TranspilerFrontendModuleParserLineClassification::ClassStatement => {
                self.on_class_statement_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::FunctionStatement => {
                self.on_class_statement_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::Comment => {
                self.on_comment_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::IndentedLine => {
                self.on_error_indented_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::JunkLine => {
                self.on_error_junk_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::EmptyLine => {
                self.on_empty_line(context, &line);
            }
        }
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        context.request_pop_due_to_end_of_file();
    }
}
