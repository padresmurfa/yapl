use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::abstract_syntax_tree::nodes::callable_facet_node::{
    AbstractSyntaxTreeCallableFacetNode,
    AbstractSyntaxTreeCallableFacetType
};
use crate::transpiler_frontend::parsers::section_parser::TranspilerFrontendSectionParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};
use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};

pub struct TranspilerFrontendCallableFacetParser {}

impl TranspilerFrontendCallableFacetParser {

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
}
