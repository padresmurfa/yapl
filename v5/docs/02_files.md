# Files

YAPL considers files of source code to be nothing more than containers for modules, which are named using reverse-DNS notation as popularized by many other languages.

## 1. Source file locations

Source files must be located in a file heirarchy that is consistent with the names of the modules that are found within them.

Thus a file that contains the module org.yapllang.doc.comments must be found in a file that is named one of the following (assuming a \*nix file-system's naming conventions):

* `**/com/yapllang/doc/comments.yapl`
* `**/com.yapllang.doc.comments.yapl`
* `**/com/yapllang.doc.comments.yapl`
* `**/com/yapllang/doc.comments.yapl`
* `**/com_yapllang_doc_comments.yapl`
* `**/com/yapllang_doc_comments.yapl`
* `**/com/yapllang/doc_comments.yapl`

### Why?

The most useful view of a project is typically the file-heirarchial view. This view is often rendered less effective by poor file-naming. Enforcing a relationship between a module's
reverse-DNS name and the file path seems like a good thing.

## 2. Character set

YAPL code is Unicode text encoded in UTF-8. The text is not canonicalized, so a single accented code point is distinct from the same character constructed from combining an accent
and a letter; those are treated as two code points. For simplicity, this document will use the unqualified term character to refer to a Unicode code point in the source text.

Each code point is distinct; for instance, upper and lower case letters are different characters.

YAPL files may not contain non-printable characters, except a leading UTF-8 byte-order-mark (0xEF 0xBB 0xBF), which is mandatory for all YAPL files.

### Why?

In absence of a BOM, the interpretation of the byte stream's byte-order is dependent on the reader. This seems like a bad thing. Also, some tools treat the BOM as a required magic
number. Furthermore, some tools identify files as unicode text based on whether or not they start with a BOM. Thus the optionality is thus detrimental, in spite of the intentions of its
inventors.

## 3. Newline vs CRLF

YAPL should interpret a CRLF, LFCR, and CR equally.

### Why?

Windows.
