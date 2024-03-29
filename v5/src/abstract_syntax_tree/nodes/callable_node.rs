use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::abstract_syntax_tree::nodes::callable_facet_node::AbstractSyntaxTreeCallableFacetNode;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AbstractSyntaxTreeCallableType {
    ModuleFunction,
    ModuleGeneratorFunction,
    ClassMethod,
    ClassGeneratorMethod,
    ClassConstructor,
}


#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeCallableNode {
    pub callable_type: AbstractSyntaxTreeCallableType,
    pub maybe_callable_name: Option<String>,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>,
    pub facet_nodes: Vec<AbstractSyntaxTreeCallableFacetNode>,
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeCallableNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::CallableNode;
    }

    fn as_callable_node(&self) -> Option<&AbstractSyntaxTreeCallableNode> {
        return Some(&self);
    }
    
}
