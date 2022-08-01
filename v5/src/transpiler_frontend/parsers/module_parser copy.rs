use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::prefix_comment_parser::TranspilerFrontendPrefixCommentParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNode,
    AbstractSyntaxTreeNodeIdentifier
};
use crate::abstract_syntax_tree::nodes::module_node::AbstractSyntaxTreeModuleNode;
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;

#[derive(Debug)]
pub struct TranspilerFrontendModuleParser {
    external_indentation_level: usize,
    internal_indentation_level: usize,
    maybe_module_name: Option<String>,    
    maybe_prefix_comment_parser: Option<Box<AbstractSyntaxTreePrefixCommentNode>>,
    maybe_suffix_comment: Option<String>,
    buffer: Vec<TranspilerFrontendLine>
}

#[derive(Debug)]
enum TranspilerFrontendModuleParserLineClassification {
    Comment,
    CommentEmptyLine,
    CommentHorizontalRule,
    InvalidCommentJunkInHorizontalRule,
    InvalidCommentMissingLeadingSpace,
    ClassStatement,
    FunctionStatement,
    IndentedLine,
    DedentedLine,
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
        let maybe_prefix_comment_dyn = context.maybe_pop_abstract_syntax_tree_node(external_indentation_level, AbstractSyntaxTreeNodeIdentifier::PrefixCommentNode);
        let maybe_prefix_comment = if maybe_prefix_comment_dyn.is_none() {
            None
        } else {
            Some(Box::new(maybe_prefix_comment_dyn.unwrap().as_prefix_comment_node().unwrap().clone()))
        };
        let mut result_module_parser = Box::new(TranspilerFrontendModuleParser {
            external_indentation_level: external_indentation_level,
            internal_indentation_level: external_indentation_level + 4,
            maybe_module_name: None,
            maybe_prefix_comment_parser: maybe_prefix_comment,
            maybe_suffix_comment: None,
            buffer: Vec::new()
        });

        // the lines in 'buffer' may include a prefix-comment, but certainly do end with a module statement, which may also end with a suffix-comment
        let maybe_module_name_and_remainder = line.line_text.strip_prefix("module ").unwrap().trim_start().split_once(":");
        if maybe_module_name_and_remainder.is_none() {
            result_module_parser.output.report_error_in_line(
                "A module statement must be terminated by a colon symbol".to_string(),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserModuleStatementMustBeTerminatedByColon,
                line
            );
        } else {
            let (module_name, untrimmed_remainder) = maybe_module_name_and_remainder.unwrap();
            result_module_parser.maybe_module_name = Some(module_name.to_string());
            if TranspilerFrontendModuleParser::validate_module_name(&module_name, line, &mut result_module_parser.output) {
                let remainder = untrimmed_remainder.trim_start();
                let maybe_split = remainder.split_once("--");
                if !maybe_split.is_none() {
                    let (maybe_comment_symbol, untrimmed_comment_comment) = maybe_split.unwrap();
                    let trimmed_suffix_comment = untrimmed_comment_comment.trim();
                    if !trimmed_suffix_comment.is_empty() {
                        result_module_parser.maybe_suffix_comment = Some(trimmed_suffix_comment.to_string());
                    }
                }
            } else {
                // an error will have been added to result_module_parser
            }
        }
        return result_module_parser;
    }

    pub fn validate_module_name(module_name: &str, line: &TranspilerFrontendLine, output: &mut TranspilationJobOutput) -> bool {
        let original = module_name.to_string();
        if original != original.replace("__", "_") {
            output.report_error_in_line(
                format!("Invalid module name. Found multiple sequential underscores separating terms in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else if original.ends_with("_") {
            output.report_error_in_line(
                format!("Invalid module name. Found trailing underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
             return false;
        } else if original.starts_with("_") {
            output.report_error_in_line(
                format!("Invalid module name. Found leading underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else if original.len() >= 256 {
            output.report_error_in_line(
                format!("Invalid module name. A module name may be at most 256 characters in length, which is still too much for comfort {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else if original != original.replace("..", ".") {
                output.report_error_in_line(
                    format!("Invalid module name. Found multiple sequential dots separating terms in {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                    line
                );
                return false;
        } else if original.ends_with(".") {
            output.report_error_in_line(
                format!("Invalid module name. Found trailing dot in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
                return false;
        } else if original.starts_with(".") {
            output.report_error_in_line(
                format!("Invalid module name. Found leading dot in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else {
            let reverse_dns_pattern = Regex::new(r"^[^\.]+\.[^\.]+\..+$").unwrap();
            if !reverse_dns_pattern.is_match(&original) {
                output.report_error_in_line(
                    format!("Invalid module name. A module name must contain at least two dots to be a valid reverse-DNS name {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                    line
                );
                return false;
            }
            for section in original.split(".") {                
                let starts_with_digit_or_underscore = Regex::new("^[0-9_]").unwrap();
                if starts_with_digit_or_underscore.is_match(&original) {
                    output.report_error_in_line(
                        format!("Invalid module name. A module name's components may not start with a digit or an underscore {:?}", original),
                        TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                        line
                    );
                    return false;
                }
                if section.ends_with("_") {
                    output.report_error_in_line(
                        format!("Invalid module name. A module name's components may not end with an underscore {:?}", original),
                        TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                        line
                    );
                    return false;
                }
                let contains_only_legal_characters = Regex::new("^[a-z0-9_.]+$").unwrap();
                if !contains_only_legal_characters.is_match(&original) {
                    output.report_error_in_line(
                        format!("Invalid module name. A module name's components may only contain lower-case ascii characters, digits, or underscores {:?}", original),
                        TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                        line
                    );
                    return false;
                }
            }
        }
        return true;
    }

    fn classify_line(&self, text: &String) -> TranspilerFrontendModuleParserLineClassification {
        return self.classify_line_impl(text, self.internal_indentation_level);
    }

    fn classify_line_impl(&self, text: &String, expected_indentation_level: usize) -> TranspilerFrontendModuleParserLineClassification {
        let trimmed = text.trim_start();
        if trimmed.is_empty() {
            return TranspilerFrontendModuleParserLineClassification::EmptyLine;
        }
        
        let indentation_level = text.len() - trimmed.len();
        if indentation_level < expected_indentation_level {
            return TranspilerFrontendModuleParserLineClassification::DedentedLine;
        } else if indentation_level > expected_indentation_level {
            return TranspilerFrontendModuleParserLineClassification::IndentedLine;
        } else if trimmed.starts_with("class ") {
            // note that this may include a suffix-comment
            return TranspilerFrontendModuleParserLineClassification::ClassStatement;
        } else if trimmed.starts_with("function ") {
            // note that this may include a suffix-comment
            return TranspilerFrontendModuleParserLineClassification::FunctionStatement;
        } else if trimmed.starts_with("--") {
            let skip_past_comment_symbol = &trimmed[2..];
            if skip_past_comment_symbol.is_empty() {
                return TranspilerFrontendModuleParserLineClassification::CommentEmptyLine;
            } else if skip_past_comment_symbol.starts_with("-") {
                // horizontal-rule
                let tmp = skip_past_comment_symbol.replace("-","");
                let junk = tmp.trim();
                if !junk.is_empty() {
                    return TranspilerFrontendModuleParserLineClassification::InvalidCommentJunkInHorizontalRule;
                }
                return TranspilerFrontendModuleParserLineClassification::CommentHorizontalRule;
            } else if skip_past_comment_symbol.starts_with(" ") {
                return TranspilerFrontendModuleParserLineClassification::Comment;
            } else {
                return TranspilerFrontendModuleParserLineClassification::InvalidCommentMissingLeadingSpace;
            }
        } else {
            return TranspilerFrontendModuleParserLineClassification::JunkLine;
        }
    }

    fn on_comment_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.buffer.push(line.clone());
    }

    fn on_comment_empty_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.buffer.push(line.clone());
    }

    fn on_comment_horizontal_rule_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.buffer.push(line.clone());
    }

    fn on_comment_error_junk_in_horizontal_rule_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected junk characteers encountered in horizontal-rule comment in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendFileParserInvalidIdentedLine,
            line
        );
    }

    fn on_comment_error_missing_leading_space_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Missing leading space in comment in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendFileParserInvalidIdentedLine,
            line
        );
    }

    fn on_error_indented_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected indented line encountered in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendFileParserInvalidIdentedLine,
            line
        );
    }

    fn on_error_junk_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected initial token encountered in module scope"),
            TranspilationJobOutputErrorCode::TranspilerFrontendFileParserInvalidStartingToken,
            line
        );
    }

    fn on_empty_line(&mut self, _context: &mut TranspilerFrontendContext, _line: &TranspilerFrontendLine) {
    }

    fn on_dedented_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.emit_abstract_syntax_tree_module_node(context);
        context.request_pop(line);
    }

    fn on_class_statement_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        // todo: create a class parser
    }

    fn on_function_statement_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
    }

    fn emit_abstract_syntax_tree_module_node(&self, context: &mut TranspilerFrontendContext) {
        println!("Emitting module node to AST: {:?} {:?} {:?}", self.maybe_module_name, self.maybe_prefix_comment_parser, self.maybe_suffix_comment);
        let mut ast_comment_lines = Vec::new();
        if !self.maybe_prefix_comment_parser.is_none() {
            for input_comment_line in &self.maybe_prefix_comment_parser.as_ref().unwrap().as_prefix_comment_node().unwrap().comment_lines {
                ast_comment_lines.push(input_comment_line.clone());
            }
        }
        let node = Box::new(AbstractSyntaxTreeModuleNode {
            module_name: self.maybe_module_name.as_ref().unwrap().clone(),
            comment_lines: ast_comment_lines
        });
        context.push_abstract_syntax_tree_node(self.external_indentation_level, node);
    }
}

impl TranspilerFrontend for TranspilerFrontendModuleParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let classification = self.classify_line(&line.line_text);
        match classification {
            TranspilerFrontendModuleParserLineClassification::Comment => {
                self.on_comment_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::CommentEmptyLine => {
                self.on_comment_empty_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::CommentHorizontalRule => {
                self.on_comment_horizontal_rule_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::InvalidCommentJunkInHorizontalRule => {
                self.on_comment_error_junk_in_horizontal_rule_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::InvalidCommentMissingLeadingSpace => {
                self.on_comment_error_missing_leading_space_line(context, &line);
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
            TranspilerFrontendModuleParserLineClassification::DedentedLine => {
                self.on_dedented_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::ClassStatement => {
                self.on_class_statement_line(context, &line);
            }
            TranspilerFrontendModuleParserLineClassification::FunctionStatement => {
                self.on_function_statement_line(context, &line);
            }
        }
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.emit_abstract_syntax_tree_module_node(context);
        context.request_pop_due_to_end_of_file();
    }

    fn append_output_to(&self, other: &mut TranspilationJobOutput) {
        other.append_output_from(&self.output);
    }

    fn get_transpilation_job_output(&mut self) -> &mut TranspilationJobOutput {
        return &mut self.output;
    }
}
