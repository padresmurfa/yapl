use regex::Regex;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::section_parser::TranspilerFrontendSectionParser;
use crate::transpiler_frontend::parsers::class_parser::TranspilerFrontendClassParser;
use crate::transpiler_frontend::parsers::module_function_parser::TranspilerFrontendModuleFunctionParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::abstract_syntax_tree::nodes::AbstractSyntaxTreeNodeIdentifier;
use crate::abstract_syntax_tree::nodes::module_node::AbstractSyntaxTreeModuleNode;

#[derive(Debug, Clone)]
pub struct TranspilerFrontendModuleParser {
    section_parser: Box<TranspilerFrontendSectionParser>
}

impl TranspilerFrontendParser for TranspilerFrontendModuleParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::ModuleParser;
    }

    fn as_module_parser(&self) -> Option<&TranspilerFrontendModuleParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendModuleParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendModuleParser> {
        return Box::new(TranspilerFrontendModuleParser {
            section_parser: TranspilerFrontendSectionParser::create(
                "module",
                &TranspilerFrontendModuleParser::validate_module_name,
                external_indentation_level,
                context,
                line
            )
        });
    }

    pub fn validate_module_name(module_name: &str, line: &TranspilerFrontendLine) -> bool {
        let original = module_name.trim().to_string();
        if original != original.replace("__", "_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid module name. Found multiple sequential underscores separating terms in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else if original.ends_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid module name. Found trailing underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
             return false;
        } else if original.starts_with("_") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid module name. Found leading underscore in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else if original.len() >= 256 {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid module name. A module name may be at most 256 characters in length, which is still too much for comfort {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else if original != original.replace("..", ".") {
            TranspilationJobOutput::report_error_in_line(
                    format!("Invalid module name. Found multiple sequential dots separating terms in {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                    line
                );
                return false;
        } else if original.ends_with(".") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid module name. Found trailing dot in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
                return false;
        } else if original.starts_with(".") {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid module name. Found leading dot in {:?}", original),
                TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                line
            );
            return false;
        } else {
            let reverse_dns_pattern = Regex::new(r"^[^\.]+\.[^\.]+\..+$").unwrap();
            if !reverse_dns_pattern.is_match(&original) {
                TranspilationJobOutput::report_error_in_line(
                    format!("Invalid module name. A module name must contain at least two dots to be a valid reverse-DNS name {:?}", original),
                    TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                    line
                );
                return false;
            }
            for section in original.split(".") {                
                let starts_with_digit_or_underscore = Regex::new("^[0-9_]").unwrap();
                if starts_with_digit_or_underscore.is_match(&original) {
                    TranspilationJobOutput::report_error_in_line(
                        format!("Invalid module name. A module name's components may not start with a digit or an underscore {:?}", original),
                        TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                        line
                    );
                    return false;
                }
                if section.ends_with("_") {
                    TranspilationJobOutput::report_error_in_line(
                        format!("Invalid module name. A module name's components may not end with an underscore {:?}", original),
                        TranspilationJobOutputErrorCode::TranspilerFrontendModuleParserStatementModuleNameInvalid,
                        line
                    );
                    return false;
                }
                let contains_only_legal_characters = Regex::new("^[a-z0-9_.]+$").unwrap();
                if !contains_only_legal_characters.is_match(&original) {
                    TranspilationJobOutput::report_error_in_line(
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
    
    fn is_valid_module_subcontent(line: &String) -> bool {
        // TODO: better parsing
        return line.starts_with("class ") || line.starts_with("function ") || line.starts_with("constant ") || line.starts_with("type ");
    }

    fn create_module_subcontent(indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        // TODO: better parsing
        let trimmed_line = line.line_text.trim_start();
        if trimmed_line.starts_with("class ") {
            let parser = TranspilerFrontendClassParser::create(indentation_level, context, line);
            context.request_push(parser);
        } else if line.line_text.trim_start().starts_with("function ") {
            let parser = TranspilerFrontendModuleFunctionParser::create(indentation_level, context, line);
            context.request_push(parser);
        } else {
            println!("unknown module subcontent: {:?}", line);
        }
    }

    fn maybe_convert_section_node_to_module_node(&mut self, context: &mut TranspilerFrontendContext) {
        let maybe_section_node = context.maybe_pop_abstract_syntax_tree_node(self.section_parser.external_indentation_level, AbstractSyntaxTreeNodeIdentifier::SectionNode);
        if !maybe_section_node.is_none() {
            let section_node = maybe_section_node.as_ref().unwrap().as_section_node().unwrap();
            context.push_abstract_syntax_tree_node(
                self.section_parser.external_indentation_level, 
                    Box::new(AbstractSyntaxTreeModuleNode {
                    fully_qualified_module_name: section_node.section_name.clone(), 
                    maybe_prefix_comment: section_node.maybe_prefix_comment.clone(),
                    maybe_suffix_comment: section_node.maybe_suffix_comment.clone(),
                })
            );
        }
    }
}

impl TranspilerFrontend for TranspilerFrontendModuleParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let internal_indentation_level: usize = self.section_parser.internal_indentation_level;
        let create_module_subcontent_closure = move |context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine| {
            TranspilerFrontendModuleParser::create_module_subcontent(internal_indentation_level, context, line);
        };
        self.section_parser.append_line(&TranspilerFrontendModuleParser::is_valid_module_subcontent, &create_module_subcontent_closure, context, line);
        self.maybe_convert_section_node_to_module_node(context);
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        self.section_parser.end_of_file(context);
        self.maybe_convert_section_node_to_module_node(context);
    }
}
