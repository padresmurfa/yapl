use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::abstract_syntax_tree::nodes::class_node::AbstractSyntaxTreeClassNode;
use crate::abstract_syntax_tree::nodes::callable_node::AbstractSyntaxTreeCallableNode;

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeModuleNode {
    pub maybe_fully_qualified_module_name: Option<String>,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>,
    pub class_nodes: Vec<AbstractSyntaxTreeClassNode>,
    pub callable_nodes: Vec<AbstractSyntaxTreeCallableNode>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeModuleNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::ModuleNode;
    }

    fn as_module_node(&self) -> Option<&AbstractSyntaxTreeModuleNode> {
        return Some(&self);
    }
    
}
