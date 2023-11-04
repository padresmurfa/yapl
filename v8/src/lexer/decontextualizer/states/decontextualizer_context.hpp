#pragma once
#ifndef ORG_YAPLLANG_DECONTEXTUALIZER_CONTEXT_HPP
#define ORG_YAPLLANG_DECONTEXTUALIZER_CONTEXT_HPP

#include "include.hpp"
#include "decontextualizer_states.hpp"
#include "lexer/preprocessor/preprocessor.hpp"
#include "lexer/preprocessor/preprocessor_line.hpp"
#include "lexer/lexer_exception.hpp"
#include "../decontextualizer_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

class DecontextualizerContext {
    public:
        DecontextualizerContext(const preprocessor::PreprocessorLine &line, std::vector<DecontextualizerState>& stateStack, std::vector<size_t> &indentation);

        void pushOutputToken(const preprocessor::PreprocessorToken &token);
        void push(DecontextualizerState state, const preprocessor::PreprocessorToken &token);
        void pop(DecontextualizerState state, const preprocessor::PreprocessorToken &token);
        void pop(DecontextualizerState state);
        DecontextualizerState getCurrentState() const;
        const preprocessor::PreprocessorLine &getCurrentLine() const;
        bool emptyState() const; 

        void indent(const std::string &whitespace);
        int maybeDedent(const std::string &whitespace);
        bool wouldDedent(const std::string &whitespace) const;
        bool wouldIndent(const std::string &whitespace) const;
        size_t getIndentLength() const;

        const std::vector<preprocessor::PreprocessorToken> &getOutputTokens();
        std::vector<preprocessor::PreprocessorToken> &mutateOutputTokens();

        std::string addContextToErrorMessage(const std::string &message) const;

        DecontextualizerException decontextualizerException(const std::string& message);
        ClosingUnopenedBlockException closingUnopenedBlockException(const preprocessor::PreprocessorToken& token);
        UnknownEscapeCharacterException unknownEscapeCharacterException(const preprocessor::PreprocessorToken& token);
        InvalidTokenInThisContextException invalidTokenInThisContextException(const preprocessor::PreprocessorToken& token, const states::DecontextualizerState state, const std::string &message);
        UnclosedOpenedBlockException unclosedOpenedBlockException(const std::string &message);
        LexerException lexerException(const std::string& message);
        Exception exception(const std::string& message);

    private:
        std::vector<size_t> &indentation_;
        preprocessor::PreprocessorLine line_;
        std::vector<preprocessor::PreprocessorToken> outputTokens_;
        std::vector<DecontextualizerState>& stateStack_;
};

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_DECONTEXTUALIZER_CONTEXT_HPP
