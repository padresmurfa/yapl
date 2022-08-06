use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::abstract_syntax_tree::nodes::callable_facet_node::{
    AbstractSyntaxTreeCallableFacetNode,
    AbstractSyntaxTreeCallableFacetType
};
use crate::abstract_syntax_tree::nodes::AbstractSyntaxTreeNodeIdentifier;
use crate::transpiler_frontend::parsers::section_parser::{
    TranspilerFrontendSectionParser,
    SectionLineContentParserCreator
};
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};

#[derive(Debug, Clone)]
pub struct TranspilerFrontendCallableFacetParser {
    maybe_facet_type: Option<AbstractSyntaxTreeCallableFacetType>,
    section_parser: Box<TranspilerFrontendSectionParser>,
    sub_contents: Vec<AbstractSyntaxTreeCallableFacetNode>
}

impl TranspilerFrontendParser for TranspilerFrontendCallableFacetParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::CallableFacetParser;
    }

    fn as_callable_facet_parser(&self) -> Option<&TranspilerFrontendCallableFacetParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendCallableFacetParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendCallableFacetParser> {
        let mut facet_type = "";
        let found_facet_type = line.line_text.trim_start().split_once(":");
        if !found_facet_type.is_none() {
            let (found_left, found_remainder) = found_facet_type.unwrap();
            facet_type = found_left;
        }
        return Box::new(TranspilerFrontendCallableFacetParser {
            maybe_facet_type: TranspilerFrontendCallableFacetParser::get_callable_facet_type(facet_type),
            section_parser: TranspilerFrontendSectionParser::create_dynamically_typed_unnamed(
                facet_type,
                &TranspilerFrontendCallableFacetParser::validate_callable_facet_type,
                external_indentation_level,
                context,
                line
            ),
            sub_contents: Vec::new()
        });
    }

    pub fn validate_callable_facet_type(callable_facet_name: &str, line: &TranspilerFrontendLine) -> bool {
        let trimmed = callable_facet_name.trim().to_string();
        if !TranspilerFrontendCallableFacetParser::is_valid_callable_facet(&trimmed) {
            TranspilationJobOutput::report_error_in_line(
                format!("Invalid callable facet name. '{}' is not one of the pre-defined facets that a callable may have (e.g. returns, input, code, ...)", trimmed),
                TranspilationJobOutputErrorCode::TranspilerFrontendCallableFacetParserFacetNameInvalid,
                line
            );
            return false;
        }
        return true;
    }

    pub fn is_valid_callable_facet(line: &str) -> bool {
        return !TranspilerFrontendCallableFacetParser::get_callable_facet_type(line).is_none();
    }

    pub fn get_callable_facet_type(line: &str) -> Option<AbstractSyntaxTreeCallableFacetType> {
        let trimmed = line.trim_start().to_string() + ":";
        if trimmed.starts_with("returns:") {
            return Some(AbstractSyntaxTreeCallableFacetType::ReturnFacet);
        } else if trimmed.starts_with("emits:") {
            return Some(AbstractSyntaxTreeCallableFacetType::EmitFacet);
        } else if trimmed.starts_with("errors:") {
            return Some(AbstractSyntaxTreeCallableFacetType::ErrorFacet);
        } else if trimmed.starts_with("code:") {
            return Some(AbstractSyntaxTreeCallableFacetType::CodeFacet);
        } else if trimmed.starts_with("inputs:") {
            return Some(AbstractSyntaxTreeCallableFacetType::InputFacet);
        } else if trimmed.starts_with("preconditions:") {
            return Some(AbstractSyntaxTreeCallableFacetType::PreConditionFacet);
        } else if trimmed.starts_with("postconditions:") {
            return Some(AbstractSyntaxTreeCallableFacetType::PostConditionFacet);
        }
        return None;
    }

    fn is_valid_callable_facet_subcontent(line: &String) -> bool {
        // any indented line is considered good enough to act as subcontent for a callable facet for the time being 
        // but this is dependent on what facet type we're in
        return true;
    }

    fn create_callable_facet_subcontent(maybe_facet_type:  Option<AbstractSyntaxTreeCallableFacetType>, indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let callable_facet_subcontent = Box::new(AbstractSyntaxTreeCallableFacetNode {
            maybe_callable_facet_type: maybe_facet_type,
            indentation_level: indentation_level,
            line: line.clone(),
            maybe_prefix_comment: None, // TODO fix this
            maybe_suffix_comment: None, // TODO fix this
        });
        context.push_abstract_syntax_tree_node(indentation_level, callable_facet_subcontent);
    }

    fn invalid_create_callable_facet_subcontent(context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        panic!("invalid_create_callable_facet_subcontent {:?}", line);
    }

    fn maybe_append_sub_content_to_facet(&mut self, context: &mut TranspilerFrontendContext) {
        loop {
            let maybe_sub_content_node = context.maybe_pop_abstract_syntax_tree_node(self.section_parser.internal_indentation_level, AbstractSyntaxTreeNodeIdentifier::CallableFacetNode);
            if !maybe_sub_content_node.is_none() {
                let sub_content_node = maybe_sub_content_node.as_ref().unwrap().as_callable_facet_node().unwrap();
                self.sub_contents.push(sub_content_node.clone());
            } else {
                break;
            }
        }
    }
}

impl TranspilerFrontend for TranspilerFrontendCallableFacetParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let result = if self.maybe_facet_type.is_none() {
            let create_callable_facet_subcontent_closure = move |context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine| {
                TranspilerFrontendCallableFacetParser::invalid_create_callable_facet_subcontent(context, line);
            };
            self.section_parser.append_line(&TranspilerFrontendCallableFacetParser::is_valid_callable_facet_subcontent, &create_callable_facet_subcontent_closure, context, line)
        } else {
            let internal_indentation_level: usize = self.section_parser.internal_indentation_level;
            let facet_type = self.maybe_facet_type.unwrap();
            let create_callable_facet_subcontent_closure = move |context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine| {
                TranspilerFrontendCallableFacetParser::create_callable_facet_subcontent(Some(facet_type), internal_indentation_level, context, line);
            };
            self.section_parser.append_line(&TranspilerFrontendCallableFacetParser::is_valid_callable_facet_subcontent, &create_callable_facet_subcontent_closure, context, line)
        };
        self.maybe_append_sub_content_to_facet(context);
        return result;
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        let result = self.section_parser.end_of_file(context);
        self.maybe_append_sub_content_to_facet(context);
        return result;
    }
}
