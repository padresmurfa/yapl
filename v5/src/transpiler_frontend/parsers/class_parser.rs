use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::section_parser::TranspilerFrontendSectionParser;
use crate::transpiler_frontend::parsers::class_facet_parser::TranspilerFrontendClassFacetParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::class_node::AbstractSyntaxTreeClassNode;
use crate::abstract_syntax_tree::nodes::AbstractSyntaxTreeNodeIdentifier;

#[derive(Debug, Clone)]
pub struct TranspilerFrontendClassParser {
    section_parser: Box<TranspilerFrontendSectionParser>
}

impl TranspilerFrontendParser for TranspilerFrontendClassParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::ClassParser;
    }

    fn as_class_parser(&self) -> Option<&TranspilerFrontendClassParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendClassParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendClassParser> {
        return Box::new(TranspilerFrontendClassParser {
            section_parser: TranspilerFrontendSectionParser::create(
                "class",
                &TranspilerFrontendClassParser::validate_class_name,
                external_indentation_level,
                context,
                line
            )
        });
    }

    pub fn validate_class_name(class_name: &str, line: &TranspilerFrontendLine) -> bool {
        let original = class_name.trim().to_string();
        if original != original.replace("__", "_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class name. Found multiple sequential underscores separating terms in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassNameInvalid,
                line
            );
            return false;
        } else if original.ends_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class name. Found trailing underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassNameInvalid,
                line
            );
             return false;
        } else if original.starts_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class name. Found leading underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassNameInvalid,
                line
            );
            return false;
        } else if original.len() >= 256 {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class name. A class name may be at most 256 characters in length, which is still too much for comfort {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassNameInvalid,
                line
            );
            return false;
        } else {
            let starts_with_digit = Regex::new("^[0-9]").unwrap();
            if starts_with_digit.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid class name. A class name may not start with a digit {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassNameInvalid,
                    line
                );
                return false;
            }
            let contains_only_legal_characters = Regex::new("^[a-z0-9_]+$").unwrap();
            if !contains_only_legal_characters.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid class name. A class name may only contain lower-case ascii characters or underscores {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassNameInvalid,
                    line
                );
                return false;
            }
        }
        return true;
    }
    
    fn is_valid_class_facet(line: &String) -> bool {
        for keyword in ["public ", "private ", "protected "] {
            if line.starts_with(keyword) {
                let maybe_facet = line.split_once(" ");
                if !maybe_facet.is_none() {
                    let (_, remainder) = maybe_facet.unwrap();
                    if remainder.starts_with("facet ") {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    fn create_class_facet(indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let parser = TranspilerFrontendClassFacetParser::create(indentation_level, context, line);
        context.request_push(parser);
    }

    fn maybe_convert_section_node_to_class_node(&mut self, context: &mut TranspilerFrontendContext) {
        let maybe_section_node = context.maybe_pop_abstract_syntax_tree_node(self.section_parser.external_indentation_level, AbstractSyntaxTreeNodeIdentifier::ClassNode);
        if !maybe_section_node.is_none() {
            let section_node = maybe_section_node.as_ref().unwrap().as_section_node().unwrap();
            context.push_abstract_syntax_tree_node(
                self.section_parser.external_indentation_level, 
                    Box::new(AbstractSyntaxTreeClassNode {
                        class_name: section_node.section_name.clone(), 
                        maybe_prefix_comment: section_node.maybe_prefix_comment.clone(),
                        maybe_suffix_comment: section_node.maybe_suffix_comment.clone(),
                    }
                )
            );
        }
    }
}

impl TranspilerFrontend for TranspilerFrontendClassParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let internal_indentation_level: usize = self.section_parser.internal_indentation_level;
        let create_class_facet_closure = move |context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine| {
            TranspilerFrontendClassParser::create_class_facet(internal_indentation_level, context, line);
        };
        self.section_parser.append_line(&TranspilerFrontendClassParser::is_valid_class_facet, &create_class_facet_closure, context, line);
        self.maybe_convert_section_node_to_class_node(context);
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.section_parser.end_of_file(context);
        self.maybe_convert_section_node_to_class_node(context);
    }
}
