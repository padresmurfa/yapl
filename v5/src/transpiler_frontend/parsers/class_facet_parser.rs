use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::section_parser::TranspilerFrontendSectionParser;
use crate::transpiler_frontend::parsers::class_method_parser::TranspilerFrontendClassMethodParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::class_facet_node::AbstractSyntaxTreeClassFacetNode;
use crate::abstract_syntax_tree::nodes::AbstractSyntaxTreeNodeIdentifier;

#[derive(Debug, Clone)]
pub struct TranspilerFrontendClassFacetParser {
    section_parser: Box<TranspilerFrontendSectionParser>
}

impl TranspilerFrontendParser for TranspilerFrontendClassFacetParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::ClassFacetParser;
    }

    fn as_class_facet_parser(&self) -> Option<&TranspilerFrontendClassFacetParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendClassFacetParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendClassFacetParser> {
        return Box::new(TranspilerFrontendClassFacetParser {
            section_parser: TranspilerFrontendSectionParser::create_with_visibility(
                "facet",
                &TranspilerFrontendClassFacetParser::validate_class_facet_name,
                external_indentation_level,
                context,
                line
            )
        });
    }

    pub fn validate_class_facet_name(class_facet_name: &str, line: &TranspilerFrontendLine) -> bool {
        let original = class_facet_name.trim().to_string();
        if original != original.replace("__", "_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class facet name. Found multiple sequential underscores separating terms in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassFacetNameInvalid,
                line
            );
            return false;
        } else if original.ends_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class facet name. Found trailing underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassFacetNameInvalid,
                line
            );
             return false;
        } else if original.starts_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class facet name. Found leading underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassFacetNameInvalid,
                line
            );
            return false;
        } else if original.len() >= 256 {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid class facet name. A class name may be at most 256 characters in length, which is still too much for comfort {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassFacetNameInvalid,
                line
            );
            return false;
        } else {
            let starts_with_digit = Regex::new("^[0-9]").unwrap();
            if starts_with_digit.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid class facet name. A class name may not start with a digit {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassFacetNameInvalid,
                    line
                );
                return false;
            }
            let contains_only_legal_characters = Regex::new("^[a-z0-9_]+$").unwrap();
            if !contains_only_legal_characters.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid class facet name. A class facet name may only contain lower-case ascii characters or underscores {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementClassFacetNameInvalid,
                    line
                );
                return false;
            }
        }
        return true;
    }
    
    fn is_valid_class_facet_content(line: &String) -> bool {
        if line.starts_with("--") {
            return true;
        }
        if line.starts_with("constructor ") || line.starts_with("method ") || line.starts_with("generator ") {
            return true;
        }
        let split_result = line.split_once(" ");
        if split_result.is_none() {
            return false;
        }
        let (_, remainder) = split_result.unwrap();
        if remainder.starts_with("is ") || remainder.starts_with("references ") {
            return true;
        }
        return false;
    }

    fn create_class_facet_subcontent(internal_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        if line.line_text.trim_start().starts_with("method ") {
            let parser = TranspilerFrontendClassMethodParser::create(internal_indentation_level, context, line);
            context.request_push(parser);
        } else {
            println!("TODO: handle class subcontent: {:?}", line);
        }
    }

    fn maybe_convert_section_node_to_class_facet_node(&mut self, context: &mut TranspilerFrontendContext) {
        let maybe_section_node = context.maybe_pop_abstract_syntax_tree_node(self.section_parser.external_indentation_level, AbstractSyntaxTreeNodeIdentifier::ClassNode);
        if !maybe_section_node.is_none() {
            let section_node = maybe_section_node.as_ref().unwrap().as_section_node().unwrap();
            context.push_abstract_syntax_tree_node(
                self.section_parser.external_indentation_level, 
                    Box::new(AbstractSyntaxTreeClassFacetNode {
                        maybe_section_visibility: section_node.maybe_section_visibility.clone(),
                        class_facet_name: section_node.section_name.clone(), 
                        maybe_prefix_comment: section_node.maybe_prefix_comment.clone(),
                        maybe_suffix_comment: section_node.maybe_suffix_comment.clone(),
                    }
                )
            );
        }
    }
}

impl TranspilerFrontend for TranspilerFrontendClassFacetParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let internal_indentation_level = self.section_parser.internal_indentation_level;
        let create_class_facet_closure = move |context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine| {
            TranspilerFrontendClassFacetParser::create_class_facet_subcontent(internal_indentation_level, context, line);
        };
        self.section_parser.append_line(&TranspilerFrontendClassFacetParser::is_valid_class_facet_content, &create_class_facet_closure, context, line);
        self.maybe_convert_section_node_to_class_facet_node(context);
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.section_parser.end_of_file(context);
        self.maybe_convert_section_node_to_class_facet_node(context);
    }
}
