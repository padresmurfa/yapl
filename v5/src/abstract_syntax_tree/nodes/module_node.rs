use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeModuleNode {
    pub module_name: String,
    pub prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub suffix_comment: Option<String>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeModuleNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::ModuleNode;
    }

    fn as_module_node(&self) -> Option<&AbstractSyntaxTreeModuleNode> {
        return Some(&self);
    }
    
}
