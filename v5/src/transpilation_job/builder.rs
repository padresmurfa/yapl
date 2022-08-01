use std::path::PathBuf;
use std::fs;

use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use crate::transpilation_job::TranspilationJob;

pub struct TranspilationJobBuilder {
    is_source_filename_invalid: bool,
    abs_source_filename: Option<String>,
    is_target_dirname_invalid: bool,
    abs_target_dirname: Option<String>
}

impl Clone for TranspilationJobBuilder  {
    fn clone(&self) -> Self {
        return TranspilationJobBuilder {
            is_source_filename_invalid: self.is_source_filename_invalid,
            is_target_dirname_invalid: self.is_target_dirname_invalid,
            abs_source_filename: self.abs_source_filename.clone(),
            abs_target_dirname: self.abs_target_dirname.clone()
        }
    }
}

impl TranspilationJobBuilder {

    pub fn create() -> TranspilationJobBuilder {
        return TranspilationJobBuilder  {
            is_source_filename_invalid: false,
            is_target_dirname_invalid: false,
            abs_source_filename: None,
            abs_target_dirname: None
        };
    }

    pub fn set_source_filename(&mut self, source_filename: &String) -> TranspilationJobBuilder  {
        let pathbuf_source_filename = PathBuf::from(source_filename);
        let canonical_source_filename_result = fs::canonicalize(pathbuf_source_filename);
        if canonical_source_filename_result.is_err() {
            self.is_source_filename_invalid = true;
            TranspilationJobOutput::report_error(
                format!("ERROR: invalid source file ({})", source_filename),
                TranspilationJobOutputErrorCode::BuilderInvalidSourceFile
            );
        } else {
            let canonical_source_filename = canonical_source_filename_result.unwrap();
            self.abs_source_filename = Some(canonical_source_filename.into_os_string().into_string().unwrap());
        }
        return self.clone();
    }

    pub fn set_target_dirname(&mut self, target_dirname: &String) -> TranspilationJobBuilder  {
        let pathbuf_target_dirname = PathBuf::from(target_dirname);
        let canonical_target_dirname_result = fs::canonicalize(pathbuf_target_dirname);
        if canonical_target_dirname_result.is_err() {
            self.is_target_dirname_invalid = true;
            TranspilationJobOutput::report_error(
                format!("ERROR: invalid target dir ({})", target_dirname),
                TranspilationJobOutputErrorCode::BuilderInvalidTargetDir
            );
        } else {
            let canonical_target_dirname = canonical_target_dirname_result.unwrap();
            self.abs_target_dirname = Some(canonical_target_dirname.into_os_string().into_string().unwrap());
        }
        return self.clone();
    }

    pub fn build(&mut self) -> Result<TranspilationJob, TranspilationJobOutputErrorCode> {
        if !TranspilationJobOutput::was_successful() {
            return Err(TranspilationJobOutput::get_error_code());
        } else if self.abs_source_filename.is_none() || self.abs_target_dirname.is_none() {
            return Err(TranspilationJobOutputErrorCode::BuilderMissingRequiredConfiguration);
        } else {
            return Ok(TranspilationJob::create(&self.abs_source_filename.as_ref().unwrap(), &self.abs_target_dirname.as_ref().unwrap()));
        }
    }
}
