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

#[derive(Debug, Clone)]
pub struct TranspilerFrontendCallableReturnFacetParser {
    section_parser: Box<TranspilerFrontendSectionParser>,
    facet_contents: Vec<TranspilerFrontendLine>
}

impl TranspilerFrontendParser for TranspilerFrontendCallableReturnFacetParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::CallableReturnFacetParser;
    }

    fn as_callable_return_facet_parser(&self) -> Option<&TranspilerFrontendCallableReturnFacetParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendCallableReturnFacetParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendCallableReturnFacetParser> {
        return Box::new(TranspilerFrontendCallableReturnFacetParser {
            section_parser: TranspilerFrontendSectionParser::create_unnamed(
                "returns",
                external_indentation_level,
                context,
                line
            ),
            facet_contents: Vec::new()
        });
    }

    fn is_valid_facet_content(line: &String) -> bool {
        // TODO not goood...
        return true;
    }

    fn create_facet_content(indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        // TODO: probably not the right thing to do here...
    }

    fn invalid_create_callable_facet_subcontent(context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        panic!("invalid_create_callable_facet_subcontent {:?}", line);
    }

    fn maybe_convert_section_node_to_callable_facet_node(&mut self, context: &mut TranspilerFrontendContext) {
    }
}

impl TranspilerFrontend for TranspilerFrontendCallableReturnFacetParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        let internal_indentation_level: usize = self.section_parser.internal_indentation_level;
        let create_facet_content_closure = move |context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine| {
            TranspilerFrontendCallableReturnFacetParser::create_facet_content(internal_indentation_level, context, line);
        };
        let result = self.section_parser.append_line(&TranspilerFrontendCallableReturnFacetParser::is_valid_facet_content, &create_facet_content_closure, context, line);
        self.maybe_convert_section_node_to_callable_facet_node(context);
        return result;
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        let result = self.section_parser.end_of_file(context);
        self.maybe_convert_section_node_to_callable_facet_node(context);
        return result;
    }
}
