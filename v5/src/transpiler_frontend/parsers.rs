pub mod class_facet_parser;
pub mod class_parser;
pub mod file_parser;
pub mod callable_parser;
pub mod callable_facet_parser;
pub mod module_function_parser;
pub mod class_method_parser;
pub mod module_parser;
pub mod section_parser;
pub mod prefix_comment_parser;

use crate::transpiler_frontend::TranspilerFrontend;

#[derive(PartialEq)]
pub enum TranspilerFrontendParserIdentifier {
    CallableFacetParser,
    CallableParser,
    ClassParser,
    FileParser,
    ModuleParser,
    PrefixCommentParser,
    SectionParser,
    ClassFacetParser
}

pub trait TranspilerFrontendParser : TranspilerFrontend {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier;

    fn as_callable_facet_parser(&self) -> Option<&callable_facet_parser::TranspilerFrontendCallableFacetParser> { return None; }
    fn as_callable_parser(&self) -> Option<&callable_parser::TranspilerFrontendCallableParser> { return None; }
    fn as_class_facet_parser(&self) -> Option<&class_facet_parser::TranspilerFrontendClassFacetParser> { return None; }
    fn as_class_parser(&self) -> Option<&class_parser::TranspilerFrontendClassParser> { return None; }
    fn as_file_parser(&self) -> Option<&file_parser::TranspilerFrontendFileParser> { return None; }
    fn as_module_parser(&self) -> Option<&module_parser::TranspilerFrontendModuleParser> { return None; }
    fn as_prefix_comment_parser(&self) -> Option<&prefix_comment_parser::TranspilerFrontendPrefixCommentParser> { return None; }
    fn as_section_parser(&self) -> Option<&section_parser::TranspilerFrontendSectionParser> { return None; }
}
