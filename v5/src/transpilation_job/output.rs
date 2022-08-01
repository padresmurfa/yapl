use std::process::ExitCode;

use super::super::transpiler_frontend::line::TranspilerFrontendLine;

#[derive(Debug)]
pub struct TranspilationJobOutputItem {
    pub message: String,
    pub line: Option<TranspilerFrontendLine>
}

impl Clone for TranspilationJobOutputItem  {
    fn clone(&self) -> Self {
        return TranspilationJobOutputItem {
            message: self.message.clone(),
            line: self.line.clone()
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum TranspilationJobOutputErrorCode {
    MainMissingCommandLineArguments = 1,
    BuilderInvalidSourceFile = 2,
    BuilderInvalidTargetDir = 3,
    BuilderMissingRequiredConfiguration = 4,
    TranspilationJobFailedToOpenSourceFile = 5,
    TranspilationJobFailedToReadSourceLine = 6,
    TranspilerFrontendModuleParserModuleStatementMustBeTerminatedByColon = 7,
    TranspilerFrontendModuleParserStatementModuleNameInvalid = 8,
    TranspilerFrontendFileParserInvalidIdentedLine = 9,
    TranspilerFrontendFileParserInvalidStartingToken = 10,
    TranspilerFrontendModuleParserClassStatementMustBeTerminatedByColon = 11,
    TranspilerFrontendClassParserStatementClassNameInvalid = 12,
    TranspilerFrontendPrefixCommentLineJunkInHorizontalRule = 13,
    TranspilerFrontendPrefixCommentLineMissingLeadingSpace = 14,
    TranspilerFrontendModuleParserInvalidIdentedLine = 15,
    TranspilerFrontendModuleParserInvalidStartingToken = 16
}

#[derive(Debug)]
pub struct TranspilationJobOutput {
    error_code: Option<TranspilationJobOutputErrorCode>,
    output: Vec<TranspilationJobOutputItem>
}

impl Clone for TranspilationJobOutput  {
    fn clone(&self) -> Self {
        let mut cloned_output = Vec::new();
        for i in 0..self.output.len() {
            cloned_output.push(self.output[i].clone());
        }
        return TranspilationJobOutput {
            error_code: self.error_code.clone(),
            output: cloned_output
        }
    }
}

impl TranspilationJobOutput {

    pub fn create() -> TranspilationJobOutput {
        return TranspilationJobOutput {
            error_code: None,
            output: Vec::new()
        };
    }

    pub fn append_output_to(&self, other: &mut TranspilationJobOutput) {
        other.append_output_from(&self);
    }

    pub fn append_output_from(&mut self, other: &TranspilationJobOutput) {
        for i in 0..other.output.len() {
            self.output.push(other.output[i].clone());
        }
    }

    pub fn was_successful(&self) -> bool {
        return self.error_code.is_none();
    }

    pub fn report_info(&mut self, message: String) {
        self.output.push(TranspilationJobOutputItem {
            message: message,
            line: None
        });
    }

    pub fn report_error(&mut self, message: String, error_code: TranspilationJobOutputErrorCode) {
        if self.error_code.is_none() {
            self.error_code = Some(error_code);
        }
        self.output.push(TranspilationJobOutputItem {
            message: message,
            line: None
        });
    }

    pub fn report_error_in_line(&mut self, message: String, error_code: TranspilationJobOutputErrorCode, line: &TranspilerFrontendLine) {
        if self.error_code.is_none() {
            self.error_code = Some(error_code);
        }
        self.output.push(TranspilationJobOutputItem {
            message: message,
            line: Some(line.clone())
        });
    }

    pub fn get_error_code(&self) -> TranspilationJobOutputErrorCode {
        return self.error_code.expect("This function should only be called if an error has occurred");
    }

    pub fn get_exit_code(&self) -> ExitCode {
        if self.error_code.is_none() {
            return ExitCode::from(0);
        }
        return ExitCode::from(self.error_code.unwrap() as u8);
    }
    
    pub fn get_transpilation_output_len(&self) -> usize {
        return self.output.len();
    }

    pub fn get_transpilation_output_message(&self, num: usize) -> TranspilationJobOutputItem {
        return TranspilationJobOutputItem { 
            message: self.output[num].message.clone(),
            line: self.output[num].line.clone()
        };
    }
}
