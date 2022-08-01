pub mod file_parser;
pub mod module_parser;
pub mod prefix_comment_parser;

#[derive(PartialEq)]
pub enum TranspilerFrontendParserIdentifier {
    FileParser,
    ModuleParser,
    PrefixCommentParser
}

pub trait TranspilerFrontendParser {
    fn get_parser_type_identifier() -> TranspilerFrontendParserIdentifier;

    fn as_file_parser(&self) -> Option<&file_parser::TranspilerFrontendFileParser> { return None; }
    fn as_module_parser(&self) -> Option<&module_parser::TranspilerFrontendModuleParser> { return None; }
    fn as_prefix_comment_parser(&self) -> Option<&prefix_comment_parser::TranspilerFrontendPrefixCommentParser> { return None; }
}
