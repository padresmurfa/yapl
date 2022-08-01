use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::prefix_comment_parser::TranspilerFrontendPrefixCommentParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::section_node::AbstractSyntaxTreeSectionNode;
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};

#[derive(Debug, Clone)]
pub struct TranspilerFrontendSectionParser {
    pub section_type: String,
    pub external_indentation_level: usize,
    pub internal_indentation_level: usize,
    pub maybe_section_name: Option<String>,    
    pub maybe_prefix_comment_parser: Option<Box<AbstractSyntaxTreePrefixCommentNode>>,
    pub maybe_suffix_comment: Option<String>
}

enum TranspilerFrontendSectionParserLineClassification {
    CommentLine,
    IndentedLine,
    DedentedLine,
    ContentLine,
    JunkLine,
    EmptyLine
}

// section-name, line
type SectionNameValidator = dyn Fn(&str, &TranspilerFrontendLine) -> bool;
type SectionLineContentClassifier = dyn Fn(&String) -> bool;
type SectionLineContentParserCreator = dyn Fn(&mut TranspilerFrontendContext, &TranspilerFrontendLine);

impl TranspilerFrontendSectionParser {

    pub fn create(section_type: &str, section_name_validator: &SectionNameValidator, external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendSectionParser> {
        let maybe_prefix_comment_dyn = context.maybe_pop_abstract_syntax_tree_node(external_indentation_level, AbstractSyntaxTreeNodeIdentifier::PrefixCommentNode);
        let maybe_prefix_comment = if maybe_prefix_comment_dyn.is_none() {
            None
        } else {
            Some(Box::new(maybe_prefix_comment_dyn.unwrap().as_prefix_comment_node().unwrap().clone()))
        };
        let mut result_section_parser = Box::new(TranspilerFrontendSectionParser {
            section_type: section_type.to_string(),
            external_indentation_level: external_indentation_level,
            internal_indentation_level: external_indentation_level + 4,
            maybe_section_name: None,
            maybe_prefix_comment_parser: maybe_prefix_comment,
            maybe_suffix_comment: None
        });

        let section_type_with_trailing_space: String = (result_section_parser.section_type.clone() + " ").to_string();
        let maybe_section_name_and_remainder = line.line_text.trim_start().strip_prefix(&section_type_with_trailing_space).unwrap().split_once(":");
        if maybe_section_name_and_remainder.is_none() {
            TranspilationJobOutput::report_error_in_line(
                format!("A {}-section-declaration statement must be terminated by a colon symbol", result_section_parser.section_type).to_string(),
                TranspilationJobOutputErrorCode::TranspilerFrontendSectionParserStatementMustBeTerminatedByColon,
                line
            );
        } else {
            let (section_name, untrimmed_remainder) = maybe_section_name_and_remainder.unwrap();
            result_section_parser.maybe_section_name = Some(section_name.to_string());
            if section_name_validator(&section_name, line) {
                let remainder = untrimmed_remainder.trim_start();
                let maybe_split = remainder.split_once("--");
                if !maybe_split.is_none() {
                    let (maybe_comment_symbol, untrimmed_comment_comment) = maybe_split.unwrap();
                    let trimmed_suffix_comment = untrimmed_comment_comment.trim();
                    if !trimmed_suffix_comment.is_empty() {
                        result_section_parser.maybe_suffix_comment = Some(trimmed_suffix_comment.to_string());
                    }
                }
            } else {
                // an error will have been added to result_section_parser
            }
        }
        return result_section_parser;
    }

    fn classify_line(&self, content_classifier: &SectionLineContentClassifier, text: &String) -> TranspilerFrontendSectionParserLineClassification {
        return self.classify_line_impl(content_classifier, text, self.internal_indentation_level);
    }

    fn classify_line_impl(&self, content_classifier: &SectionLineContentClassifier, text: &String, expected_indentation_level: usize) -> TranspilerFrontendSectionParserLineClassification {
        let trimmed = text.trim_start();
        if trimmed.is_empty() {
            return TranspilerFrontendSectionParserLineClassification::EmptyLine;
        }
        let indentation_level = text.len() - trimmed.len();
        if indentation_level < expected_indentation_level {
            return TranspilerFrontendSectionParserLineClassification::DedentedLine;
        } else if indentation_level > expected_indentation_level {
            return TranspilerFrontendSectionParserLineClassification::IndentedLine;
        } else if trimmed.starts_with("--") {
            return TranspilerFrontendSectionParserLineClassification::CommentLine;
        } else if content_classifier(&trimmed.to_string()) {
            return TranspilerFrontendSectionParserLineClassification::ContentLine;
        } else {
            return TranspilerFrontendSectionParserLineClassification::JunkLine;
        }
    }

    fn on_comment_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let parser = TranspilerFrontendPrefixCommentParser::create(self.internal_indentation_level, context, line);
        context.request_push(parser);
    }

    fn on_error_indented_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected indented line encountered in {}'s {}-section scope", self.maybe_section_name.as_ref().unwrap(), self.section_type),
            TranspilationJobOutputErrorCode::TranspilerFrontendSectionParserInvalidIdentedLine,
            line
        );
    }

    fn on_error_junk_line(&mut self, _context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        TranspilationJobOutput::report_error_in_line(
            format!("Unexpected initial token encountered in {}'s {}-section scope", self.maybe_section_name.as_ref().unwrap(), self.section_type),
            TranspilationJobOutputErrorCode::TranspilerFrontendSectionParserInvalidStartingToken,
            line
        );
    }

    fn on_empty_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
    }

    fn on_content_line(&mut self, content_creator: &SectionLineContentParserCreator, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        content_creator(context, line);
    }

    fn on_dedented_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.emit_abstract_syntax_tree_section_node(context);
        context.request_pop(line);
    }

    fn emit_abstract_syntax_tree_section_node(&self, context: &mut TranspilerFrontendContext) {
        println!("Emitting {}-section node to AST: {:?} {:?} {:?}", self.section_type, self.maybe_section_name, self.maybe_prefix_comment_parser, self.maybe_suffix_comment);
        let maybe_prefix_comment = if self.maybe_prefix_comment_parser.is_none() {
            None
        } else {
            let prefix_comment_node = self.maybe_prefix_comment_parser.as_ref().unwrap().as_prefix_comment_node().unwrap().clone();
            Some(prefix_comment_node)
        };
        let maybe_suffix_comment = if self.maybe_suffix_comment.is_none() {
            None
        } else {
            Some(self.maybe_suffix_comment.as_ref().unwrap().clone())
        };
        let section_name = self.maybe_section_name.as_ref().unwrap().clone();
        let node = Box::new(AbstractSyntaxTreeSectionNode {
            section_name: section_name,
            maybe_prefix_comment: maybe_prefix_comment,
            maybe_suffix_comment: maybe_suffix_comment
        });
        context.push_abstract_syntax_tree_node(self.external_indentation_level, node);
    }

    pub fn append_line(&mut self, content_classifier: &SectionLineContentClassifier, content_creator: &SectionLineContentParserCreator, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let classification = self.classify_line(content_classifier, &line.line_text);
        match classification {
            TranspilerFrontendSectionParserLineClassification::CommentLine => {
                self.on_comment_line(context, &line);
            }
            TranspilerFrontendSectionParserLineClassification::ContentLine => {
                self.on_content_line(content_creator, context, &line);
            }
            TranspilerFrontendSectionParserLineClassification::IndentedLine => {
                self.on_error_indented_line(context, &line);
            }
            TranspilerFrontendSectionParserLineClassification::JunkLine => {
                self.on_error_junk_line(context, &line);
            }
            TranspilerFrontendSectionParserLineClassification::EmptyLine => {
                self.on_empty_line(context, &line);
            }
            TranspilerFrontendSectionParserLineClassification::DedentedLine => {
                self.on_dedented_line(context, &line);
            }
        }
    }

    pub fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.emit_abstract_syntax_tree_section_node(context);
        context.request_pop_due_to_end_of_file();
    }
}
