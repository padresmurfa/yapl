pub mod parsers;
pub mod context;
pub mod line;

use crate::transpilation_job::output::TranspilationJobOutput;

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;

pub trait TranspilerFrontend : std::fmt::Debug {
    fn append_line(&mut self, context: &mut TranspilerFrontendContext, line: &TranspilerFrontendLine);
    fn end_of_file(&mut self, context: &mut TranspilerFrontendContext);
    fn append_output_to(&self, other: &mut TranspilationJobOutput);
    fn get_transpilation_job_output(&mut self) -> &mut TranspilationJobOutput;
}
