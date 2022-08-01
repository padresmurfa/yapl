use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::{
    AbstractSyntaxTreePrefixCommentNode,
    AbstractSyntaxTreePrefixCommentNodeValue
};

#[derive(Debug, Clone)]
pub struct TranspilerFrontendPrefixCommentParser {
    external_indentation_level: usize,
    internal_indentation_level: usize,
    buffer: Vec<PrefixCommentItem>,
    output: TranspilationJobOutput
}

#[derive(Debug, Clone)]
enum TranspilerFrontendPrefixCommentParserLineClassification {
    PrefixComment,
    PrefixCommentEmptyLine,
    PrefixCommentHorizontalRule,
    InvalidPrefixCommentJunkInHorizontalRule,
    InvalidPrefixCommentMissingLeadingSpace,
    EndOfPrefixComment
}

#[derive(Debug, Clone)]
struct PrefixCommentItem {
    classification: TranspilerFrontendPrefixCommentParserLineClassification,
    line: TranspilerFrontendLine,
}

impl TranspilerFrontendParser for TranspilerFrontendPrefixCommentParser {
    fn get_parser_type_identifier() -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::PrefixCommentParser;
    }
    fn as_prefix_comment_parser(&self) -> Option<&TranspilerFrontendPrefixCommentParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendPrefixCommentParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<dyn TranspilerFrontend> {
        let mut result = Box::new(TranspilerFrontendPrefixCommentParser {
            external_indentation_level: external_indentation_level,
            internal_indentation_level: external_indentation_level,
            buffer: Vec::new(),
            output: TranspilationJobOutput::create()
        });
        result.append_line(context, line);
        return result;
    }

    fn classify_line(&self, text: &String) -> TranspilerFrontendPrefixCommentParserLineClassification {
        return self.classify_line_at_indentation_level(text, self.internal_indentation_level);
    }

    fn classify_line_at_indentation_level(&self, text: &String, expected_indentation_level: usize) -> TranspilerFrontendPrefixCommentParserLineClassification {
        let trimmed = text.trim_start();
        if trimmed.is_empty() {
            return TranspilerFrontendPrefixCommentParserLineClassification::EndOfPrefixComment;
        }
        let indentation_level = text.len() - trimmed.len();
        if indentation_level < expected_indentation_level {
            return TranspilerFrontendPrefixCommentParserLineClassification::EndOfPrefixComment;
        } else if indentation_level > expected_indentation_level {
            return TranspilerFrontendPrefixCommentParserLineClassification::EndOfPrefixComment;
        } else if trimmed.starts_with("--") {
            let skip_past_comment_symbol = &trimmed[2..];
            if skip_past_comment_symbol.is_empty() {
                return TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentEmptyLine;
            } else if skip_past_comment_symbol.starts_with("-") {
                // horizontal-rule
                let tmp = skip_past_comment_symbol.replace("-","");
                let junk = tmp.trim();
                if !junk.is_empty() {
                    return TranspilerFrontendPrefixCommentParserLineClassification::InvalidPrefixCommentJunkInHorizontalRule;
                }
                return TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentHorizontalRule;
            } else if skip_past_comment_symbol.starts_with(" ") {
                return TranspilerFrontendPrefixCommentParserLineClassification::PrefixComment;
            } else {
                return TranspilerFrontendPrefixCommentParserLineClassification::InvalidPrefixCommentMissingLeadingSpace;
            }
        } else {
            return TranspilerFrontendPrefixCommentParserLineClassification::EndOfPrefixComment;
        }
    }

    fn on_prefix_comment_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.buffer.push(
            PrefixCommentItem {
                classification: TranspilerFrontendPrefixCommentParserLineClassification::PrefixComment, 
                line: line.clone()
            }
        );
    }

    fn on_prefix_comment_empty_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.buffer.push(
            PrefixCommentItem {
                classification: TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentEmptyLine, 
                line: line.clone()
            }
        );
    }

    fn on_prefix_comment_horizontal_rule_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.buffer.push(
            PrefixCommentItem {
                classification: TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentHorizontalRule, 
                line: line.clone()
            }
        );
    }

    fn on_error_invalid_prefix_comment_junk_in_horizontal_rule_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.output.report_error_in_line(
            format!("Unexpected junk characters encountered in horizontal-rule prefix-comment"),
            TranspilationJobOutputErrorCode::TranspilerFrontendPrefixCommentLineJunkInHorizontalRule,
            line
        );
    }

    fn on_error_invalid_prefix_comment_missing_leading_space_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.output.report_error_in_line(
            format!("Missing leading space in comment in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendPrefixCommentLineMissingLeadingSpace,
            line
        );
    }

    fn on_error_junk_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.output.report_error_in_line(
            format!("Unexpected initial token encountered in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendFileParserInvalidStartingToken,
            line
        );
    }

    fn on_end_of_prefix_comment_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.push_abstract_syntax_tree_prefix_comment_node(context);
        context.request_pop(line);        
    }

    fn push_abstract_syntax_tree_prefix_comment_node(&mut self, context: &mut TranspilerFrontendContext) {
        let mut ast_comment_lines = Vec::new();
        for prefix_comment_line in &self.buffer {
            let classification = self.classify_line_at_indentation_level(&prefix_comment_line.line.line_text, self.external_indentation_level);
            match classification {
                TranspilerFrontendPrefixCommentParserLineClassification::PrefixComment => {
                    ast_comment_lines.push(AbstractSyntaxTreePrefixCommentNodeValue::Comment(prefix_comment_line.line.line_text.trim_start()[3..].to_string()));
                }
                TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentEmptyLine => {
                    ast_comment_lines.push(AbstractSyntaxTreePrefixCommentNodeValue::EmptyLine);
                }
                TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentHorizontalRule => {
                    ast_comment_lines.push(AbstractSyntaxTreePrefixCommentNodeValue::HorizontalRule);
                }
                _ => {
                    panic!("didn't expect {:?} {:?}", classification, prefix_comment_line.line.line_text);
                }
            }
        }
        let node = Box::new(AbstractSyntaxTreePrefixCommentNode {
            comment_lines: ast_comment_lines
        });
        context.push_abstract_syntax_tree_node(self.external_indentation_level, node);
    }

}

impl TranspilerFrontend for TranspilerFrontendPrefixCommentParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let classification = self.classify_line(&line.line_text);
        match classification {
            TranspilerFrontendPrefixCommentParserLineClassification::PrefixComment => {
                self.on_prefix_comment_line(context, &line);
            }
            TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentEmptyLine => {
                self.on_prefix_comment_empty_line(context, &line);
            }
            TranspilerFrontendPrefixCommentParserLineClassification::PrefixCommentHorizontalRule => {
                self.on_prefix_comment_horizontal_rule_line(context, &line);
            }
            TranspilerFrontendPrefixCommentParserLineClassification::InvalidPrefixCommentJunkInHorizontalRule => {
                self.on_error_invalid_prefix_comment_junk_in_horizontal_rule_line(context, &line);
            }
            TranspilerFrontendPrefixCommentParserLineClassification::InvalidPrefixCommentMissingLeadingSpace => {
                self.on_error_invalid_prefix_comment_missing_leading_space_line(context, &line);
            }
            TranspilerFrontendPrefixCommentParserLineClassification::EndOfPrefixComment => {
                self.on_end_of_prefix_comment_line(context, &line);
            }
        }
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.push_abstract_syntax_tree_prefix_comment_node(context);
        context.request_pop_due_to_end_of_file();
    }

    fn append_output_to(&self, other: &mut TranspilationJobOutput) {
        other.append_output_from(&self.output);
    }

    fn get_transpilation_job_output(&mut self) -> &mut TranspilationJobOutput {
        return &mut self.output;
    }
}
