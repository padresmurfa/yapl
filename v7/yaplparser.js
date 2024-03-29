/**
 * LR parser generated by the Syntax tool.
 *
 * https://www.npmjs.com/package/syntax-cli
 *
 *   npm install -g syntax-cli
 *
 *   syntax-cli --help
 *
 * To regenerate run:
 *
 *   syntax-cli \
 *     --grammar ~/path-to-grammar-file \
 *     --mode <parsing-mode> \
 *     --output ~/path-to-output-parser-file.js
 */

'use strict';

/**
 * Matched token text.
 */
let yytext;

/**
 * Length of the matched token text.
 */
let yyleng;

/**
 * Storage object.
 */
let yy = {};

/**
 * Result of semantic action.
 */
let __;

/**
 * Result location object.
 */
let __loc;

function yyloc(start, end) {
  if (!yy.options.captureLocations) {
    return null;
  }

  // Epsilon doesn't produce location.
  if (!start || !end) {
    return start || end;
  }

  return {
    startOffset: start.startOffset,
    endOffset: end.endOffset,
    startLine: start.startLine,
    endLine: end.endLine,
    startColumn: start.startColumn,
    endColumn: end.endColumn,
  };
}

const EOF = '$';

/**
 * List of productions (generated by Syntax tool).
 */
const productions = [[-1,1,(_1,_1loc) => { __loc = yyloc(_1loc, _1loc);__ = _1 }],
[0,1,(_1,_1loc) => { __loc = yyloc(_1loc, _1loc);__ = [_1] }],
[0,3,(_1,_2,_3,_1loc,_2loc,_3loc) => { __loc = yyloc(_1loc, _3loc);__ = _1; _1.push(_3) }],
[0,2,(_1,_2,_1loc,_2loc) => { __loc = yyloc(_1loc, _2loc);__ = _1; }],
[1,1,(_1,_1loc) => { __loc = yyloc(_1loc, _1loc);__ = _1 }],
[2,1,(_1,_1loc) => { __loc = yyloc(_1loc, _1loc);__ = _1 }],
[2,0,() => { __loc = null;__ = null }],
[3,3,(_1,_2,_3,_1loc,_2loc,_3loc) => { __loc = yyloc(_1loc, _3loc);__ = _2 }],
[3,4,(_1,_2,_3,_4,_1loc,_2loc,_3loc,_4loc) => { __loc = yyloc(_1loc, _4loc);__ = _2 }],
[3,3,(_1,_2,_3,_1loc,_2loc,_3loc) => { __loc = yyloc(_1loc, _3loc);__ = _2 }],
[4,3,(_1,_2,_3,_1loc,_2loc,_3loc) => { __loc = yyloc(_1loc, _3loc);__ = yyparse.YAPLModule(__loc, _2) }]];

/**
 * Encoded tokens map.
 */
const tokens = {"NL":"5","INDENT":"6","SEMANTIC_COMMENT":"7","DEDENT":"8","KEYWORD_MODULE":"9","DOT_DELIMITED_IDENTIFIER":"10","$":"11"};

/**
 * Parsing table (generated by Syntax tool).
 */
const table = [{"0":1,"1":2,"4":3,"9":"s4"},{"5":"s5","11":"acc"},{"5":"r1","8":"r1","11":"r1"},{"5":"r4","8":"r4","11":"r4"},{"10":"s7"},{"1":6,"4":3,"5":"r3","8":"r3","9":"s4","11":"r3"},{"5":"r2","8":"r2","11":"r2"},{"2":8,"3":9,"5":"r6","6":"s10","8":"r6","11":"r6"},{"5":"r10","8":"r10","11":"r10"},{"5":"r5","8":"r5","11":"r5"},{"0":12,"1":2,"4":3,"7":"s11","9":"s4"},{"0":14,"1":2,"4":3,"8":"s13","9":"s4"},{"5":"s5","8":"s16"},{"5":"r7","8":"r7","11":"r7"},{"5":"s5","8":"s15"},{"5":"r8","8":"r8","11":"r8"},{"5":"r9","8":"r9","11":"r9"}];

/**
 * Parsing stack.
 */
const stack = [];

/**
 * Tokenizer instance.
 */
let tokenizer;
/**
 * Generic tokenizer used by the parser in the Syntax tool.
 *
 * https://www.npmjs.com/package/syntax-cli
 *
 * See `--custom-tokinzer` to skip this generation, and use a custom one.
 */

const lexRules = [[/^;[ a-zA-Z]*/, function() { yytext = yytext.slice(1, ); return 'SEMANTIC_COMMENT'; }],
[/^module/, function() { return 'KEYWORD_MODULE' }],
[/^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+/, function() { return 'DOT_DELIMITED_IDENTIFIER' }],
[/^[a-zA-Z0-9_]+/, function() { return 'IDENTIFIER' }],
[/^:\n((    )*)/, function() { 

        yytext = yytext.slice(2); // strip leading : and NL
        const matchedIndent = yytext.length;

        // On new block creation, we expect indent level to go up:

        if (matchedIndent < currentIndent) {
          throw new Error(
            'Bad indent: got ' + matchedIndent +
            ', expected > ' + currentIndent
          );
        }

        // Init the indent level. All the following indentations
        // should be relative to it.

        if (!indentLevel) {
          indentLevel = matchedIndent;
          // console.log("initialising the indent level to " + indentLevel)
        }

        currentIndent = matchedIndent;
        return 'INDENT';
       }],
[/^\n((    )*)/, function() { 
        yytext = yytext.slice(1); // strip leading NL
        const matchedIndent = yytext.length;

        // console.log('digging dedent');

        // 1. Stay in the same block, skip NL.

        if (matchedIndent === currentIndent) {
          yytext = "";
          // console.log('returning NL at matchedIndent=' + matchedIndent + ", currentIndent=" + currentIndent)
          return 'NL';
        }

        // 2. Else it should be a dedent ...

        if (matchedIndent < currentIndent) {
          // console.log('returning NL and DEDENTS')

          // If we dedent on several levels, we return several
          // dedent tokens, plus 'NL' token. So dedenting from level 3
          // to level 1, may look like: ['DEDENT', 'DEDENT', 'NL']

          const dedentTokensCount = (currentIndent - matchedIndent) / indentLevel;
          const tokens = new Array(dedentTokensCount).fill('DEDENT');

          // The "fake" NL token is to make BNF grammar simpler.
          tokens.push('NL');

          currentIndent = matchedIndent;
          return tokens;
        }

        // 3. or a bad indent
        if (currentIndent !== 0) {
          throw new Error(
            'Blocks should start with ":", ' +
            'cannot increase indent not in block' +
            ", matchedIndent: " + matchedIndent +
            ", currentIndent: " + currentIndent +
            ", yytext: " + yytext
          );
        }

        // 4. or an empty line
        // console.log('got an empty line');
        yytext = "";
       }],
[/^\s+/, function() { /* skip whitespace */ }]];
const lexRulesByConditions = {"INITIAL":[0,1,2,3,4,5,6]};

const EOF_TOKEN = {
  type: EOF,
  value: '',
};

tokenizer = {
  initString(string) {
    this._string = string;
    this._cursor = 0;

    this._states = ['INITIAL'];
    this._tokensQueue = [];

    this._currentLine = 1;
    this._currentColumn = 0;
    this._currentLineBeginOffset = 0;

    /**
     * Matched token location data.
     */
    this._tokenStartOffset = 0;
    this._tokenEndOffset = 0;
    this._tokenStartLine = 1;
    this._tokenEndLine = 1;
    this._tokenStartColumn = 0;
    this._tokenEndColumn = 0;

    return this;
  },

  /**
   * Returns tokenizer states.
   */
  getStates() {
    return this._states;
  },

  getCurrentState() {
    return this._states[this._states.length - 1];
  },

  pushState(state) {
    this._states.push(state);
  },

  begin(state) {
    this.pushState(state);
  },

  popState() {
    if (this._states.length > 1) {
      return this._states.pop();
    }
    return this._states[0];
  },

  getNextToken() {
    // Something was queued, return it.
    if (this._tokensQueue.length > 0) {
      return this.onToken(this._toToken(this._tokensQueue.shift()));
    }

    if (!this.hasMoreTokens()) {
      return this.onToken(EOF_TOKEN);
    }

    let string = this._string.slice(this._cursor);
    let lexRulesForState = lexRulesByConditions[this.getCurrentState()];

    for (let i = 0; i < lexRulesForState.length; i++) {
      let lexRuleIndex = lexRulesForState[i];
      let lexRule = lexRules[lexRuleIndex];

      let matched = this._match(string, lexRule[0]);

      // Manual handling of EOF token (the end of string). Return it
      // as `EOF` symbol.
      if (string === '' && matched === '') {
        this._cursor++;
      }

      if (matched !== null) {
        yytext = matched;
        yyleng = yytext.length;
        let token = lexRule[1].call(this);

        if (!token) {
          return this.getNextToken();
        }

        // If multiple tokens are returned, save them to return
        // on next `getNextToken` call.

        if (Array.isArray(token)) {
          const tokensToQueue = token.slice(1);
          token = token[0];
          if (tokensToQueue.length > 0) {
            this._tokensQueue.unshift(...tokensToQueue);
          }
        }

        return this.onToken(this._toToken(token, yytext));
      }
    }

    if (this.isEOF()) {
      this._cursor++;
      return EOF_TOKEN;
    }

    this.throwUnexpectedToken(
      string[0],
      this._currentLine,
      this._currentColumn
    );
  },

  /**
   * Throws default "Unexpected token" exception, showing the actual
   * line from the source, pointing with the ^ marker to the bad token.
   * In addition, shows `line:column` location.
   */
  throwUnexpectedToken(symbol, line, column) {
    const lineSource = this._string.split('\n')[line - 1];
    let lineData = '';

    if (lineSource) {
      const pad = ' '.repeat(column);
      lineData = '\n\n' + lineSource + '\n' + pad + '^\n';
    }

    throw new SyntaxError(
      `${lineData}Unexpected token: "${symbol}" ` +
      `at ${line}:${column}.`
    );
  },

  getCursor() {
    return this._cursor;
  },

  getCurrentLine() {
    return this._currentLine;
  },

  getCurrentColumn() {
    return this._currentColumn;
  },

  _captureLocation(matched) {
    const nlRe = /\n/g;

    // Absolute offsets.
    this._tokenStartOffset = this._cursor;

    // Line-based locations, start.
    this._tokenStartLine = this._currentLine;
    this._tokenStartColumn =
      this._tokenStartOffset - this._currentLineBeginOffset;

    // Extract `\n` in the matched token.
    let nlMatch;
    while ((nlMatch = nlRe.exec(matched)) !== null) {
      this._currentLine++;
      this._currentLineBeginOffset = this._tokenStartOffset + nlMatch.index + 1;
    }

    this._tokenEndOffset = this._cursor + matched.length;

    // Line-based locations, end.
    this._tokenEndLine = this._currentLine;
    this._tokenEndColumn = this._currentColumn =
      (this._tokenEndOffset - this._currentLineBeginOffset);
  },

  _toToken(tokenType, yytext = '') {
    return {
      // Basic data.
      type: tokenType,
      value: yytext,

      // Location data.
      startOffset: this._tokenStartOffset,
      endOffset: this._tokenEndOffset,
      startLine: this._tokenStartLine,
      endLine: this._tokenEndLine,
      startColumn: this._tokenStartColumn,
      endColumn: this._tokenEndColumn,
    };
  },

  isEOF() {
    return this._cursor === this._string.length;
  },

  hasMoreTokens() {
    return this._cursor <= this._string.length;
  },

  _match(string, regexp) {
    let matched = string.match(regexp);
    if (matched) {
      // Handle `\n` in the matched token to track line numbers.
      this._captureLocation(matched[0]);
      this._cursor += matched[0].length;
      return matched[0];
    }
    return null;
  },

  /**
   * Allows analyzing, and transforming token. Default implementation
   * just passes the token through.
   */
  onToken(token) {
    return token;
  },
};

/**
 * Expose tokenizer so it can be accessed in semantic actions.
 */
yy.lexer = tokenizer;
yy.tokenizer = tokenizer;

/**
 * Global parsing options. Some options can be shadowed per
 * each `parse` call, if the optations are passed.
 *
 * Initalized to the `captureLocations` which is passed
 * from the generator. Other options can be added at runtime.
 */
yy.options = {
  captureLocations: true,
};

// helper functions for errors
function unexpectedToken(token) {
  if (token.type === EOF) {
    unexpectedEndOfInput();
  }

  tokenizer.throwUnexpectedToken(
    token.value,
    token.startLine,
    token.startColumn
  );
}

function parseError(message) {
  throw new SyntaxError(message);
}

function unexpectedEndOfInput() {
  parseError(`Unexpected end of input.`);
}

/**
 * Parsing module.
 */
const yyparse = {
  /**
   * Sets global parsing options.
   */
  setOptions(options) {
    yy.options = options;
    return this;
  },

  /**
   * Returns parsing options.
   */
  getOptions() {
    return yy.options;
  },

  /**
   * Parses a string.
   */
  parse(string, parseOptions) {
    if (!tokenizer) {
      throw new Error(`Tokenizer instance wasn't specified.`);
    }

    tokenizer.initString(string);

    /**
     * If parse options are passed, override global parse options for
     * this call, and later restore global options.
     */
    let globalOptions = yy.options;
    if (parseOptions) {
      yy.options = Object.assign({}, yy.options, parseOptions);
    }

    /**
     * Allow callers to do setup work based on the
     * parsing string, and passed options.
     */
    yyparse.onParseBegin(string, tokenizer, yy.options);

    stack.length = 0;
    stack.push(0);

    let token = tokenizer.getNextToken();
    let shiftedToken = null;

    do {
      if (!token) {
        // Restore options.
        yy.options = globalOptions;
        unexpectedEndOfInput();
      }
      let state = stack[stack.length - 1];
      let column = tokens[token.type];

      if (!table[state].hasOwnProperty(column)) {
        yy.options = globalOptions;
        unexpectedToken(token);
      }

      let entry = table[state][column];

      // Shift action.
      if (entry[0] === 's') {
        let loc = null;

        if (yy.options.captureLocations) {
          loc = {
            startOffset: token.startOffset,
            endOffset: token.endOffset,
            startLine: token.startLine,
            endLine: token.endLine,
            startColumn: token.startColumn,
            endColumn: token.endColumn,
          };
        }

        shiftedToken = this.onShift(token);

        stack.push(
          {symbol: tokens[shiftedToken.type], semanticValue: shiftedToken.value, loc},
          Number(entry.slice(1))
        );

        token = tokenizer.getNextToken();
      }

      // Reduce action.
      else if (entry[0] === 'r') {
        let productionNumber = entry.slice(1);
        let production = productions[productionNumber];
        let hasSemanticAction = typeof production[2] === 'function';
        let semanticValueArgs = hasSemanticAction ? [] : null;

        const locationArgs = (
          hasSemanticAction && yy.options.captureLocations
            ? []
            : null
        );

        if (production[1] !== 0) {
          let rhsLength = production[1];
          while (rhsLength-- > 0) {
            stack.pop();
            let stackEntry = stack.pop();

            if (hasSemanticAction) {
              semanticValueArgs.unshift(stackEntry.semanticValue);

              if (locationArgs) {
                locationArgs.unshift(stackEntry.loc);
              }
            }
          }
        }

        const reduceStackEntry = {symbol: production[0]};

        if (hasSemanticAction) {
          yytext = shiftedToken ? shiftedToken.value : null;
          yyleng = shiftedToken ? shiftedToken.value.length : null;

          const semanticActionArgs = (
            locationArgs !== null
              ? semanticValueArgs.concat(locationArgs)
              : semanticValueArgs
          );

          production[2](...semanticActionArgs);

          reduceStackEntry.semanticValue = __;

          if (locationArgs) {
            reduceStackEntry.loc = __loc;
          }
        }

        const nextState = stack[stack.length - 1];
        const symbolToReduceWith = production[0];

        stack.push(
          reduceStackEntry,
          table[nextState][symbolToReduceWith]
        );
      }

      // Accept.
      else if (entry === 'acc') {
        stack.pop();
        let parsed = stack.pop();

        if (stack.length !== 1 ||
            stack[0] !== 0 ||
            tokenizer.hasMoreTokens()) {
          // Restore options.
          yy.options = globalOptions;
          unexpectedToken(token);
        }

        if (parsed.hasOwnProperty('semanticValue')) {
          yy.options = globalOptions;
          yyparse.onParseEnd(parsed.semanticValue);
          return parsed.semanticValue;
        }

        yyparse.onParseEnd();

        // Restore options.
        yy.options = globalOptions;
        return true;
      }

    } while (tokenizer.hasMoreTokens() || stack.length > 1);
  },

  setTokenizer(customTokenizer) {
    tokenizer = customTokenizer;
    return yyparse;
  },

  getTokenizer() {
    return tokenizer;
  },

  onParseBegin(string, tokenizer, options) {},
  onParseEnd(parsed) {},

  /**
   * Allows analyzing, and transforming shifted token. Default implementation
   * just passes the token through.
   */
  onShift(token) {
    return token;
  }
};


    /**
     * Indentation level in YAPL is mandated at 4 characters.
     */
    let indentLevel = 4;

    /**
     * Current level of indentation.
     */
    let currentIndent = 0;

    // Event handlers.

    yyparse.onParseBegin = (string, tokenizer, options) => {
      console.log('Parsing code:', string);
    };

    yyparse.onParseEnd = (parsed) => {
      // console.log('Parsed value:', JSON.stringify(parsed));
    };

    yyparse.onShift = (token) => {
      console.log('Shifting token:', token);
      return token;
    },

    yyparse.YAPLStatement = (location, id, statements) => {
      if (statements === null) {
        return { location, id };
      }
      return { type: "STATEMENT", location, id, statements };
    }
  
    yyparse.YAPLModule = (location, id) => {
      return { type: "MODULE", location, id };
    }
    

module.exports = yyparse;
