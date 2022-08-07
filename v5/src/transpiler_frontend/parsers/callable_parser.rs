use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::section_parser::TranspilerFrontendSectionParser;
use crate::transpiler_frontend::parsers::callable_facet_parser::TranspilerFrontendCallableFacetParser;
use crate::transpiler_frontend::parsers::callable_return_facet_parser::TranspilerFrontendCallableReturnFacetParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::abstract_syntax_tree::nodes::callable_node::{
    AbstractSyntaxTreeCallableNode,
    AbstractSyntaxTreeCallableType
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::AbstractSyntaxTreeNodeIdentifier;
use crate::abstract_syntax_tree::nodes::callable_facet_node::AbstractSyntaxTreeCallableFacetType;

#[derive(Debug, Clone)]
pub struct TranspilerFrontendCallableParser {
    callable_type: AbstractSyntaxTreeCallableType,
    section_parser: Box<TranspilerFrontendSectionParser>
}

impl TranspilerFrontendParser for TranspilerFrontendCallableParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::CallableParser;
    }

    fn as_callable_parser(&self) -> Option<&TranspilerFrontendCallableParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendCallableParser {

    pub fn create(callable_type: AbstractSyntaxTreeCallableType, external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendCallableParser> {
        let callable_type_str = match callable_type {
            AbstractSyntaxTreeCallableType::ModuleFunction => "function",
            AbstractSyntaxTreeCallableType::ModuleGeneratorFunction => "generator",
            AbstractSyntaxTreeCallableType::ClassMethod => "method",
            AbstractSyntaxTreeCallableType::ClassGeneratorMethod => "generator",
            AbstractSyntaxTreeCallableType::ClassConstructor => "constructor"
        };
        if callable_type == AbstractSyntaxTreeCallableType::ClassConstructor {
            return Box::new(TranspilerFrontendCallableParser {
                callable_type: callable_type,
                section_parser: TranspilerFrontendSectionParser::create_unnamed(
                    callable_type_str,
                    external_indentation_level,
                    context,
                    line
                )
            });
        } else {
            return Box::new(TranspilerFrontendCallableParser {
                callable_type: callable_type,
                section_parser: TranspilerFrontendSectionParser::create(
                    callable_type_str,
                    &TranspilerFrontendCallableParser::validate_callable_name,
                    external_indentation_level,
                    context,
                    line
                )
            });
        }
    }

    pub fn validate_callable_name(callable_name: &str, line: &TranspilerFrontendLine) -> bool {
        let original = callable_name.trim().to_string();
        if original != original.replace("__", "_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid callable name. Found multiple sequential underscores separating terms in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendCallableParserStatementCallableNameInvalid,
                line
            );
            return false;
        } else if original.ends_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid callable name. Found trailing underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendCallableParserStatementCallableNameInvalid,
                line
            );
             return false;
        } else if original.starts_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid callable name. Found leading underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendCallableParserStatementCallableNameInvalid,
                line
            );
            return false;
        } else if original.len() >= 256 {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid callable name. A callable name may be at most 256 characters in length, which is still too much for comfort {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendCallableParserStatementCallableNameInvalid,
                line
            );
            return false;
        } else {
            let starts_with_digit = Regex::new("^[0-9]").unwrap();
            if starts_with_digit.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid callable name. A callable name may not start with a digit {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendCallableParserStatementCallableNameInvalid,
                    line
                );
                return false;
            }
            let contains_only_legal_characters = Regex::new("^[a-z0-9_]+$").unwrap();
            if !contains_only_legal_characters.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid callable name. A callable name may only contain lower-case ascii characters or underscores {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendCallableParserStatementCallableNameInvalid,
                    line
                );
                return false;
            }
        }
        return true;
    }
    
    fn is_valid_callable_subcontent(line: &String) -> bool {
        return TranspilerFrontendCallableFacetParser::is_valid_callable_facet(line);
    }

    fn create_callable_subcontent(indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let classification = TranspilerFrontendCallableFacetParser::get_callable_facet_type(&line.line_text);
        if classification == Some(AbstractSyntaxTreeCallableFacetType::ReturnFacet) {
            let parser = TranspilerFrontendCallableReturnFacetParser::create(indentation_level, context, line);
            context.request_push(parser);
        }
    }

    fn maybe_convert_section_node_to_callable_node(&mut self, context: &mut TranspilerFrontendContext) {
        let maybe_section_node = context.maybe_pop_abstract_syntax_tree_node(self.section_parser.external_indentation_level, AbstractSyntaxTreeNodeIdentifier::SectionNode);
        if !maybe_section_node.is_none() {
            let section_node = maybe_section_node.as_ref().unwrap().as_section_node().unwrap();
            let mut facet_nodes = Vec::new();
            loop {
                let maybe_facet_node = context.maybe_pop_abstract_syntax_tree_node(self.section_parser.internal_indentation_level, AbstractSyntaxTreeNodeIdentifier::CallableFacetNode);
                if !maybe_facet_node.is_none() {
                    let facet_node = maybe_facet_node.as_ref().unwrap().as_callable_facet_node().unwrap();
                    facet_nodes.push(facet_node.clone());
                } else {
                    break;
                }
            }
            context.push_abstract_syntax_tree_node(
                self.section_parser.external_indentation_level, 
                    Box::new(AbstractSyntaxTreeCallableNode {
                        callable_type: self.callable_type,
                        maybe_callable_name: section_node.maybe_section_name.clone(), 
                        maybe_prefix_comment: section_node.maybe_prefix_comment.clone(),
                        maybe_suffix_comment: section_node.maybe_suffix_comment.clone(),
                        facet_nodes: facet_nodes
                    }
                )
            );
        }
    }
}

impl TranspilerFrontend for TranspilerFrontendCallableParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let internal_indentation_level: usize = self.section_parser.internal_indentation_level;
        let create_callable_subcontent_closure = move |context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine| {
            TranspilerFrontendCallableParser::create_callable_subcontent(internal_indentation_level, context, line);
        };
        self.section_parser.append_line(&TranspilerFrontendCallableParser::is_valid_callable_subcontent, &create_callable_subcontent_closure, context, line);
        self.maybe_convert_section_node_to_callable_node(context);
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.section_parser.end_of_file(context);
        self.maybe_convert_section_node_to_callable_node(context);
    }
}
