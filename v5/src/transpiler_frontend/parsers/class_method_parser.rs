use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::callable_parser::TranspilerFrontendCallableParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};

#[derive(Debug, Clone)]
pub struct TranspilerFrontendClassMethodParser {
    callable_parser: Box<TranspilerFrontendCallableParser>
}

impl TranspilerFrontendParser for TranspilerFrontendClassMethodParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::ClassMethodParser;
    }

    fn as_class_method_parser(&self) -> Option<&TranspilerFrontendClassMethodParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendClassMethodParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendClassMethodParser> {
        let class_method_parser = Box::new(TranspilerFrontendCallableParser::create(
            "method",
            external_indentation_level,
            context,
            line
        ).as_callable_parser().unwrap().clone());
        return Box::new(TranspilerFrontendClassMethodParser {
            callable_parser: class_method_parser
        });
    }
}

impl TranspilerFrontend for TranspilerFrontendClassMethodParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        return self.callable_parser.append_line(context, line);
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        return self.callable_parser.end_of_file(context);
    }
}
