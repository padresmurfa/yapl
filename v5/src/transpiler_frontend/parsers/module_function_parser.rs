use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::TranspilerFrontend;
use crate::transpiler_frontend::parsers::callable_parser::TranspilerFrontendCallableParser;
use crate::transpiler_frontend::parsers::{
    TranspilerFrontendParser,
    TranspilerFrontendParserIdentifier
};

#[derive(Debug, Clone)]
pub struct TranspilerFrontendModuleFunctionParser {
    callable_parser: Box<TranspilerFrontendCallableParser>
}

impl TranspilerFrontendParser for TranspilerFrontendModuleFunctionParser {
    fn get_parser_type_identifier(&self) -> TranspilerFrontendParserIdentifier {
        return TranspilerFrontendParserIdentifier::ModuleFunctionParser;
    }

    fn as_module_function_parser(&self) -> Option<&TranspilerFrontendModuleFunctionParser> {
        return Some(&self);
    }
}

impl TranspilerFrontendModuleFunctionParser {

    pub fn create(external_indentation_level: usize, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) -> Box<TranspilerFrontendModuleFunctionParser> {
        let module_function_parser = Box::new(TranspilerFrontendCallableParser::create(
            "function",
            external_indentation_level,
            context,
            line
        ).as_callable_parser().unwrap().clone());
        return Box::new(TranspilerFrontendModuleFunctionParser {
            callable_parser: module_function_parser
        });
    }
}

impl TranspilerFrontend for TranspilerFrontendModuleFunctionParser {

    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine) {
        return self.callable_parser.append_line(context, line);
    }

    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext) {
        return self.callable_parser.end_of_file(context);
    }
}
