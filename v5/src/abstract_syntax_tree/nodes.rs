pub mod class_facet_node;
pub mod class_node;
pub mod module_node;
pub mod prefix_comment_node;
pub mod section_node;
pub mod callable_node;
pub mod callable_facet_node;

#[derive(PartialEq)]
pub enum AbstractSyntaxTreeNodeIdentifier {
    ClassFacetNode,
    CallableFacetNode,
    ClassNode,
    CallableNode,
    ModuleNode,
    PrefixCommentNode,
    SectionNode
}

pub trait AbstractSyntaxTreeNode : std::fmt::Debug {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier;

    fn as_callable_facet_node(&self) -> Option<&callable_facet_node::AbstractSyntaxTreeCallableFacetNode> { return None; }
    fn as_callable_node(&self) -> Option<&callable_node::AbstractSyntaxTreeCallableNode> { return None; }
    fn as_class_facet_node(&self) -> Option<&class_facet_node::AbstractSyntaxTreeClassFacetNode> { return None; }
    fn as_class_node(&self) -> Option<&class_node::AbstractSyntaxTreeClassNode> { return None; }
    fn as_module_node(&self) -> Option<&module_node::AbstractSyntaxTreeModuleNode> { return None; }
    fn as_prefix_comment_node(&self) -> Option<&prefix_comment_node::AbstractSyntaxTreePrefixCommentNode> { return None; }
    fn as_section_node(&self) -> Option<&section_node::AbstractSyntaxTreeSectionNode> { return None; }
}
