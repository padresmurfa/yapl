use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::transpiler_frontend::line::TranspilerFrontendLine;

#[derive(Debug, Clone, Copy)]
pub enum AbstractSyntaxTreeCallableFacetType {
    ReturnFacet,
    EmitFacet,
    ErrorFacet,
    CodeFacet,
    InputFacet,
    PreConditionFacet,
    PostConditionFacet
}

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeCallableFacetSubContentNode {
    pub maybe_callable_facet_type: Option<AbstractSyntaxTreeCallableFacetType>,
    pub line: TranspilerFrontendLine, // todo: this is not how we move info from frontend to the AST
    pub indentation_level: usize,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeCallableFacetSubContentNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::ClassFacetSubContentNode;
    }

    fn as_callable_facet_sub_content_node(&self) -> Option<&AbstractSyntaxTreeCallableFacetSubContentNode> {
        return Some(&self);
    }
    
}
