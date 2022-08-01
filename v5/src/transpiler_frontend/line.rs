use crate::transpilation_job::output::TranspilationJobOutput;

#[derive(Debug, Clone)]
pub struct TranspilerFrontendLine {
    pub line_number: usize,
    pub line_text: String
}

impl TranspilerFrontendLine {
    pub fn create(line_number: usize, line_text: &String) -> TranspilerFrontendLine {
        return TranspilerFrontendLine {
            line_number: line_number,
            line_text: line_text.clone()
        };
    }
}
