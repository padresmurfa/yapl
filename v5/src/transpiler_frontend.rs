pub mod parsers;
pub mod context;
pub mod line;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;

pub trait TranspilerFrontend : std::fmt::Debug {
    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine);
    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext);
}
