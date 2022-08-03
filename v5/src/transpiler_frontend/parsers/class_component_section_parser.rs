use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::section_parser::TranspilerFrontendSectionParser;
use crate::transpiler_frontend::parsers::prefix_comment_parser::TranspilerFrontendPrefixCommentParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::abstract_syntax_tree::nodes::class_node::AbstractSyntaxTreeClassNode;
use crate::abstract_syntax_tree::nodes::class_component_section_node::AbstractSyntaxTreeClassComponentSectionNode;
use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};

#[derive(Debug, Clone)]
pub struct TranspilerFrontendClassComponentSectionParser {
    section_parser: Box<TranspilerFrontendSectionParser>
}

impl TranspilerFrontendParser for TranspilerFrontendClassComponentSectionParser {
    fn get_parser_type_identifier() -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::ClassComponentSectionParser;
    }

    fn as_class_component_section_parser(&self) -> Option<&TranspilerFrontendClassComponentSectionParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendClassComponentSectionParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<dyn TranspilerFrontend> {
        return Box::new(TranspilerFrontendClassComponentSectionParser {
            section_parser: TranspilerFrontendSectionParser::create_with_visibility_and_dynamic_name(
                &TranspilerFrontendClassComponentSectionParser::validate_class_component_section_name,
                external_indentation_level,
                context,
                line
            )
        });
    }

    pub fn validate_class_component_section_name(class_component_section_name: &str, line: &TranspilerFrontendLine) -> bool {
        let original = class_component_section_name.to_string();
        if original != original.replace("__", "_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class component section name. Found multiple sequential underscores separating terms in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassComponentSectionNameInvalid,
                line
            );
            return false;
        } else if original.ends_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class component section name. Found trailing underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassComponentSectionNameInvalid,
                line
            );
             return false;
        } else if original.starts_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class component section name. Found leading underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassComponentSectionNameInvalid,
                line
            );
            return false;
        } else if original.len() >= 256 {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class component section name. A class name may be at most 256 characters in length, which is still too much for comfort {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassComponentSectionNameInvalid,
                line
            );
            return false;
        } else {
            let starts_with_digit = Regex::new("^[0-9]").unwrap();
            if starts_with_digit.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid class component section name. A class name may not start with a digit {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassComponentSectionNameInvalid,
                    line
                );
                return false;
            }
            let contains_only_legal_characters = Regex::new("^[a-z0-9_]+$").unwrap();
            if !contains_only_legal_characters.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid class component section name. A class component section name may only contain lower-case ascii characters or underscores {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassComponentSectionNameInvalid,
                    line
                );
                return false;
            }
        }
        return true;
    }
    
    fn is_valid_class_component_section_subcontent(line: &String) -> bool {
        for keyword in ["public ", "private ", "protected "] {
            if line.starts_with(keyword) {
                return true;
            }
        }
        return false;
    }

    fn create_class_component_section_subcontent(context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        println!("TODO: handle class subcontent: {:?}", line);
    }

    fn maybe_convert_section_node_to_class_component_section_node(&mut self, context: &mut TranspilerFrontendContext) {
        let maybe_section_node = context.maybe_pop_abstract_syntax_tree_node(self.section_parser.external_indentation_level, AbstractSyntaxTreeNodeIdentifier::ClassNode);
        if !maybe_section_node.is_none() {
            let section_node = maybe_section_node.as_ref().unwrap().as_section_node().unwrap();
            context.push_abstract_syntax_tree_node(
                self.section_parser.external_indentation_level, 
                    Box::new(AbstractSyntaxTreeClassComponentSectionNode {
                        maybe_section_visibility: section_node.maybe_section_visibility.clone(),
                        class_component_section_name: section_node.section_name.clone(), 
                        maybe_prefix_comment: section_node.maybe_prefix_comment.clone(),
                        maybe_suffix_comment: section_node.maybe_suffix_comment.clone(),
                    }
                )
            );
        }
    }
}

impl TranspilerFrontend for TranspilerFrontendClassComponentSectionParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        self.section_parser.append_line(&TranspilerFrontendClassComponentSectionParser::is_valid_class_component_section_subcontent, &TranspilerFrontendClassComponentSectionParser::create_class_component_section_subcontent, context, line);
        self.maybe_convert_section_node_to_class_component_section_node(context);
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.section_parser.end_of_file(context);
        self.maybe_convert_section_node_to_class_component_section_node(context);
    }
}
