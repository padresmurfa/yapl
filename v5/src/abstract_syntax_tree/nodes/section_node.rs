use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;

#[derive(Debug, Clone)]
pub enum AbstractSyntaxTreeSectionNodeVisibility {
    Public,
    Private,
    Protected
}

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeSectionNode {
    pub maybe_section_type: Option<String>,
    pub maybe_section_name: Option<String>,
    pub maybe_section_visibility: Option<AbstractSyntaxTreeSectionNodeVisibility>,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeSectionNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::SectionNode;
    }

    fn as_section_node(&self) -> Option<&AbstractSyntaxTreeSectionNode> {
        return Some(&self);
    }
    
}
