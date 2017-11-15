<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta charset="utf-8"/>
<meta name="generator" content="Docutils 0.14: http://docutils.sourceforge.net/" />
<title>collective.ttwpo</title>
<style type="text/css">

/* Minimal style sheet for the HTML output of Docutils.                    */
/*                                                                         */
/* :Author: Günter Milde, based on html4css1.css by David Goodger          */
/* :Id: $Id: minimal.css 8036 2017-02-14 13:05:46Z milde $               */
/* :Copyright: © 2015 Günter Milde.                                        */
/* :License: Released under the terms of the `2-Clause BSD license`_,      */
/*    in short:                                                            */
/*                                                                         */
/*    Copying and distribution of this file, with or without modification, */
/*    are permitted in any medium without royalty provided the copyright   */
/*    notice and this notice are preserved.                                */
/*                                                                         */
/*    This file is offered as-is, without any warranty.                    */
/*                                                                         */
/* .. _2-Clause BSD license: http://www.spdx.org/licenses/BSD-2-Clause     */

/* This CSS2.1_ stylesheet defines rules for Docutils elements without    */
/* HTML equivalent. It is required to make the document semantic visible. */
/*                                                                        */
/* .. _CSS2.1: http://www.w3.org/TR/CSS2                                  */
/* .. _validates: http://jigsaw.w3.org/css-validator/validator$link       */

/* alignment of text and inline objects inside block objects*/
.align-left   { text-align: left; }
.align-right  { text-align: right; }
.align-center { clear: both; text-align: center; }
.align-top    { vertical-align: top; }
.align-middle { vertical-align: middle; }
.align-bottom { vertical-align: bottom; }

/* titles */
h1.title, p.subtitle {
  text-align: center;
}
p.admonition-title,
p.topic-title,
p.sidebar-title,
p.rubric,
p.system-message-title {
  font-weight: bold;
}
h1 + p.subtitle,
h1 + p.section-subtitle {
  font-size: 1.6em;
}
h2 + p.section-subtitle { font-size: 1.28em; }
p.subtitle,
p.section-subtitle,
p.sidebar-subtitle {
  font-weight: bold;
  margin-top: -0.5em;
}
p.sidebar-title,
p.rubric {
  font-size: larger;
}
p.rubric { color: maroon; }
a.toc-backref {
  color: black;
  text-decoration: none; }

/* Warnings, Errors */
div.caution p.admonition-title,
div.attention p.admonition-title,
div.danger p.admonition-title,
div.error p.admonition-title,
div.warning p.admonition-title,
div.system-messages h1,
div.error,
span.problematic,
p.system-message-title {
  color: red;
}

/* inline literals */
span.docutils.literal {
  font-family: monospace;
  white-space: pre-wrap;
}
/* do not wraph at hyphens and similar: */
.literal > span.pre { white-space: nowrap; }

/* Lists */

/* compact and simple lists: no margin between items */
.simple  li, .compact li,
.simple  ul, .compact ul,
.simple  ol, .compact ol,
.simple > li p, .compact > li p,
dl.simple > dd, dl.compact > dd {
  margin-top: 0;
  margin-bottom: 0;
}

/* Table of Contents */
div.topic.contents { margin: 0; }
ul.auto-toc {
  list-style-type: none;
  padding-left: 1.5em; }

/* Enumerated Lists */
ol.arabic     { list-style: decimal }
ol.loweralpha { list-style: lower-alpha }
ol.upperalpha { list-style: upper-alpha }
ol.lowerroman { list-style: lower-roman }
ol.upperroman { list-style: upper-roman }

dt span.classifier { font-style: italic }
dt span.classifier:before {
  font-style: normal;
  margin: 0.5em;
  content: ":";
}

/* Field Lists and drivatives */
/* bold field name, content starts on the same line */
dl.field-list > dt,
dl.option-list > dt,
dl.docinfo > dt,
dl.footnote > dt,
dl.citation > dt {
  font-weight: bold;
  clear: left;
  float: left;
  margin: 0;
  padding: 0;
  padding-right: 0.5em;
}
/* Offset for field content (corresponds to the --field-name-limit option) */
dl.field-list > dd,
dl.option-list > dd,
dl.docinfo > dd {
  margin-left:  9em; /* ca. 14 chars in the test examples */
}
/* start field-body on a new line after long field names */
dl.field-list > dd > *:first-child,
dl.option-list > dd > *:first-child
{
  display: inline-block;
  width: 100%;
  margin: 0;
}
/* field names followed by a colon */
dl.field-list > dt:after,
dl.docinfo > dt:after {
  content: ":";
}

/* Bibliographic Fields (docinfo) */
pre.address { font: inherit; }
dd.authors > p { margin: 0; }

/* Option Lists */
dl.option-list { margin-left: 40px; }
dl.option-list > dt { font-weight: normal; }
span.option { white-space: nowrap; }

/* Footnotes and Citations  */
dl.footnote.superscript > dd {margin-left: 1em; }
dl.footnote.brackets > dd {margin-left: 2em; }
dl > dt.label { font-weight: normal; }
a.footnote-reference.brackets:before,
dt.label > span.brackets:before { content: "["; }
a.footnote-reference.brackets:after,
dt.label > span.brackets:after { content: "]"; }
a.footnote-reference.superscript,
dl.footnote.superscript > dt.label {
  vertical-align: super;
  font-size: smaller;
}
dt.label > span.fn-backref { margin-left: 0.2em; }
dt.label > span.fn-backref > a { font-style: italic; }

/* Line Blocks */
div.line-block { display: block; }
div.line-block div.line-block {
  margin-top: 0;
  margin-bottom: 0;
  margin-left: 40px;
}

/* Figures, Images, and Tables */
.figure.align-left,
img.align-left,
object.align-left,
table.align-left {
  margin-right: auto;
}
.figure.align-center,
img.align-center,
object.align-center {
  margin-left: auto;
  margin-right: auto;
  display: block;
}
table.align-center {
  margin-left: auto;
  margin-right: auto;
}
.figure.align-right,
img.align-right,
object.align-right,
table.align-right {
  margin-left: auto;
}
/* reset inner alignment in figures and tables */
/* div.align-left, div.align-center, div.align-right, */
table.align-left, table.align-center, table.align-right
{ text-align: inherit }

/* Admonitions and System Messages */
div.admonition,
div.system-message,
div.sidebar{
  margin: 40px;
  border: medium outset;
  padding-right: 1em;
  padding-left: 1em;
}

/* Sidebar */
div.sidebar {
  width: 30%;
  max-width: 26em;
  float: right;
  clear: right;
}

/* Text Blocks */
div.topic,
pre.literal-block,
pre.doctest-block,
pre.math,
pre.code {
  margin-right: 40px;
  margin-left: 40px;
}
pre.code .ln { color: gray; } /* line numbers */

/* Tables */
table { border-collapse: collapse; }
td, th {
  border-style: solid;
  border-color: silver;
  padding: 0 1ex;
  border-width: thin;
}
td > p:first-child, th > p:first-child { margin-top: 0; }
td > p, th > p { margin-bottom: 0; }

table > caption {
  text-align: left;
  margin-bottom: 0.25em
}

table.borderless td, table.borderless th {
  border: 0;
  padding: 0;
  padding-right: 0.5em /* separate table cells */
}

</style>
<style type="text/css">

/* CSS31_ style sheet for the output of Docutils HTML writers.             */
/* Rules for easy reading and pre-defined style variants.		   */
/*                                                                         */
/* :Author: Günter Milde, based on html4css1.css by David Goodger          */
/* :Id: $Id: plain.css 8120 2017-06-22 21:02:40Z milde $               */
/* :Copyright: © 2015 Günter Milde.                                        */
/* :License: Released under the terms of the `2-Clause BSD license`_,      */
/*    in short:                                                            */
/*                                                                         */
/*    Copying and distribution of this file, with or without modification, */
/*    are permitted in any medium without royalty provided the copyright   */
/*    notice and this notice are preserved.                                */
/*    	     	      	     	 					   */
/*    This file is offered as-is, without any warranty.                    */
/*                                                                         */
/* .. _2-Clause BSD license: http://www.spdx.org/licenses/BSD-2-Clause     */
/* .. _CSS3: http://www.w3.org/TR/CSS3		        		   */


/* Document Structure */
/* ****************** */

/* "page layout" */
body {
  padding: 0 5%;
  margin: 8px 0;
}
div.document {
  line-height:1.3;
  counter-reset: table;
  /* counter-reset: figure; */
  /* avoid long lines --> better reading */
  /* OTOH: lines should not be too short because of missing hyphenation, */
  max-width: 50em;
  margin: auto;
}

/* Sections */

/* Transitions */

hr.docutils {
  width: 80%;
  margin-top: 1em;
  margin-bottom: 1em;
  clear: both;
}

/* Paragraphs               */
/* ==========               */

/* vertical space (parskip) */
p, ol, ul, dl,
div.line-block,
table{
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}
h1, h2, h3, h4, h5, h6,
dl > dd {
  margin-bottom: 0.5em;
}

/* Lists                    */
/* ==========               */

/* Definition Lists         */

dl > dd > p:first-child { margin-top: 0; }
/* :last-child is not part of CSS 2.1 (introduced in CSS 3) */
dl > dd > p:last-child  { margin-bottom: 0; }

/* lists nested in definition lists */
/* :only-child is not part of CSS 2.1 (introduced in CSS 3) */
dd > ul:only-child, dd > ol:only-child { padding-left: 1em; }

/* Description Lists */
/* styled like in most dictionaries, encyclopedias etc. */
dl.description > dt {
  font-weight: bold;
  clear: left;
  float: left;
  margin: 0;
  padding: 0;
  padding-right: 0.5em;
}

/* Field Lists */

/* example for custom field-name width */
dl.field-list.narrow > dd {
  margin-left: 5em;
}
/* run-in: start field-body on same line after long field names */
dl.field-list.run-in > dd p {
  display: block;
}

/* Bibliographic Fields */

/* generally, bibliographic fields use special definition list dl.docinfo */
/* but dedication and abstract are placed into "topic" divs */
div.abstract p.topic-title {
  text-align: center;
}
div.dedication {
  margin: 2em 5em;
  text-align: center;
  font-style: italic;
}
div.dedication p.topic-title {
  font-style: normal;
}

/* Citations */
dl.citation dt.label {
  font-weight: bold;
}
span.fn-backref {
  font-weight: normal;
}

/* Text Blocks           */
/* ============          */

/* Literal Blocks           */
pre.literal-block, pre.doctest-block,
pre.math, pre.code {
  margin-left: 1.5em;
  margin-right: 1.5em
}

/* Block Quotes             */

blockquote,
div.topic {
  margin-left: 1.5em;
  margin-right: 1.5em
}
blockquote > table,
div.topic > table {
  margin-top: 0;
  margin-bottom: 0;
}
blockquote p.attribution,
div.topic p.attribution {
  text-align: right;
  margin-left: 20%;
}

/* Tables                   */
/* ======                   */

/* th { vertical-align: bottom; } */

table tr { text-align: left; }

/* "booktabs" style (no vertical lines) */
table.booktabs {
  border: 0;
  border-top: 2px solid;
  border-bottom: 2px solid;
  border-collapse: collapse;
}
table.booktabs * {
  border: 0;
}
table.booktabs th {
  border-bottom: thin solid;
}

/* numbered tables (counter defined in div.document) */
table.numbered > caption:before {
  counter-increment: table;
  content: "Table " counter(table) ": ";
  font-weight: bold;
}

/* Explicit Markup Blocks   */
/* ======================   */

/* Footnotes and Citations  */
/* -----------------------  */

/* line on the left */
dl.footnote {
  padding-left: 1ex;
  border-left: solid;
  border-left-width: thin;
}

/* Directives               */
/* ----------               */

/* Body Elements            */
/* ~~~~~~~~~~~~~            */

/* Images and Figures */

/* let content flow to the side of aligned images and figures */
.figure.align-left,
img.align-left,
object.align-left {
  display: block;
  clear: left;
  float: left;
  margin-right: 1em
}
.figure.align-right,
img.align-right,
object.align-right {
  display: block;
  clear: right;
  float: right;
  margin-left: 1em
}
/* Stop floating sidebars, images and figures at section level 1,2,3 */
h1, h2, h3 { clear: both; }

/* Sidebar */

/* Move into the margin. In a layout with fixed margins, */
/* it can be moved into the margin completely.		 */
div.sidebar {
  width: 30%;
  max-width: 26em;
  margin-left: 1em;
  margin-right: -5.5%;
  background-color: #ffffee ;
}

/* Code                     */

pre.code, code { background-color: #eeeeee }
pre.code .ln { color: gray; } /* line numbers */
/* basic highlighting: for a complete scheme, see */
/* http://docutils.sourceforge.net/sandbox/stylesheets/ */
pre.code .comment, code .comment { color: #5C6576 }
pre.code .keyword, code .keyword { color: #3B0D06; font-weight: bold }
pre.code .literal.string, code .literal.string { color: #0C5404 }
pre.code .name.builtin, code .name.builtin { color: #352B84 }
pre.code .deleted, code .deleted { background-color: #DEB0A1}
pre.code .inserted, code .inserted { background-color: #A3D289}

/* Math                     */
/* styled separately (see math.css for math-output=HTML) */

/* Epigraph                 */
/* Highlights               */
/* Pull-Quote               */
/* Compound Paragraph       */
/* Container                */

/* can be styled in a custom stylesheet */

/* Document Header and Footer */

div.footer, div.header {
  clear: both;
  font-size: smaller;
}

/* Inline Markup            */
/* =============            */

/* Emphasis                 */
/*   em                     */
/* Strong Emphasis          */
/*   strong		    */
/* Interpreted Text         */
/*   span.interpreted  	    */
/* Title Reference 	    */
/*   cite		    */
/* Inline Literals          */
/* possible values: normal, nowrap, pre, pre-wrap, pre-line */
/*   span.docutils.literal { white-space: pre-wrap; } */

/* Hyperlink References     */
a { text-decoration: none; }

/* External Targets         */
/*   span.target.external   */
/* Internal Targets  	    */
/*   span.target.internal   */
/* Footnote References      */
/*   a.footnote-reference   */
/* Citation References      */
/*   a.citation-reference   */

</style>
</head>
<body>
<div class="document" id="collective-ttwpo">
<h1 class="title">collective.ttwpo</h1>

<!-- This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
This text does not appear on pypi or github. It is a comment. -->
<p>Translations for Plone UI through-the-web (TTW) with option to connect to translation web-services.</p>
<div class="section" id="features">
<h1>Features</h1>
<ul class="simple">
<li><p>Create an i18n-domain and languages variants TTW (also delete them).</p></li>
<li><p>Add GNU Gettext (<span class="docutils literal">*.po</span>) files TTW to a language.</p></li>
<li><p>Manage different versions of a GNU Gettext file and set one as current.</p></li>
<li><p>Fetch GNU Gettext files from configured translations services. So far only <a class="reference external" href="http://zanata.org/">Zanata</a> is supported.</p></li>
</ul>
</div>
<div class="section" id="current-limitations">
<h1>Current Limitations</h1>
<ul class="simple">
<li><p>it is not yet possible to override global, file-system configured (zcml) i18n-domains (see todo).</p></li>
</ul>
<div class="section" id="configuring-a-webservice">
<h2>Configuring a webservice</h2>
<p>For each i18n-domain provide a JSON configuration like so:</p>
<pre class="literal-block">{
    &quot;servicename&quot;:&quot;zanata&quot;,
    &quot;url&quot;:&quot;https://zanata.mydomain.com/rest/&quot;,
    &quot;user&quot;:&quot;johndoe&quot;,
    &quot;token&quot;:&quot;abcdef1234567890abcdef1234567890&quot;,
    &quot;project&quot;: &quot;mydemo.project&quot;,
    &quot;version&quot;: &quot;1.x&quot;,
    &quot;document&quot;: &quot;zanata-document-name&quot;
}</pre>
<p>The key <span class="docutils literal">servicename</span> is mandatory and used to look a up a named adapter.
All other settings are adapter specific and are passed as-is to the adapter.</p>
</div>
</div>
<div class="section" id="installation">
<h1>Installation</h1>
<p>Install collective.ttwpo by adding it to your buildout:</p>
<pre class="literal-block">[buildout]

...

eggs =
    collective.ttwpo</pre>
<p>and then running <span class="docutils literal">bin/buildout</span>.</p>
<p>Example using the <span class="docutils literal">Zanata</span> webservice connector:</p>
<pre class="literal-block">eggs =
    collective.ttwpo[zanata]</pre>
<p>After installation activate it in the addons control-panel.
Visit the new <span class="docutils literal">TTW PO Support</span> control-panel.</p>
</div>
<div class="section" id="todo-nice-to-have">
<h1>Todo/ Nice-to-Have</h1>
<ul class="simple">
<li><p>Allow single users or groups to manage a language: create/delete/make current/sync.</p></li>
<li><p>Download uploaded PO files.</p></li>
<li><p>If an i18n-domain was already registered global, use their catalogs.
Order: First local catalog, then global catalogs.</p></li>
<li><p>Make upload capability configurable.</p></li>
<li><p>Add Transifex connector.</p></li>
<li><p>Allow environment variables in webservice configuration, which then are replaced.</p></li>
<li><p>If a webservice was configured, sync all languages at once.
Create missing languages.</p></li>
<li><p>GenericSetup import/ export of the whole configuration.</p></li>
</ul>
</div>
<div class="section" id="contributions-and-source-code">
<h1>Contributions and Source Code</h1>
<a class="reference external image-reference" href="https://travis-ci.org/collective/collective.ttwpo"><img alt="https://travis-ci.org/collective/collective.ttwpo.svg?branch=master" src="https://travis-ci.org/collective/collective.ttwpo.svg?branch=master" /></a>
<a class="reference external image-reference" href="https://coveralls.io/github/collective/collective.ttwpo?branch=master"><img alt="https://coveralls.io/repos/github/collective/collective.ttwpo/badge.svg?branch=master" src="https://coveralls.io/repos/github/collective/collective.ttwpo/badge.svg?branch=master" /></a>
<p>If you want to help with the development (improvement, update, bug-fixing, ...) of <span class="docutils literal">collective.ttwpo</span> this is a great idea!</p>
<p>The code is located in the <a class="reference external" href="https://github.com/collective/collective.ttwpo">GitHub Collective</a>.</p>
<p>You can clone it or <a class="reference external" href="https://collective.github.com/">get access to the GitHub Collective</a> and work directly on the project.</p>
<p>Maintainers are Jens Klein and the <a class="reference external" href="https://bluedynamics.com/">BlueDynamics Alliance</a> developer team.</p>
<p>We appreciate any contribution and if a release is needed to be done on pypi, please just contact one of us:
<a class="reference external" href="mailto:dev&#64;bluedynamics.com">dev&#64;bluedynamics dot com</a></p>
<p>If you are having issues, please let me know:</p>
<ul class="simple">
<li><p>File an issue at the <a class="reference external" href="https://github.com/collective/collective.ttwpo/issues">TTWPO Issue Tracker</a>.</p></li>
<li><p>or just write me an email to <a class="reference external" href="mailto:jens&#64;bluedynamics.com">jens&#64;bluedynamics.com</a>.</p></li>
</ul>
<p>This code was initially written for and paid by <a class="reference external" href="https://www.porscheinformatik.at/">Porsche Informatik Gesellschaft m.b.H.</a>, Salzburg.</p>
</div>
<div class="section" id="license">
<h1>License</h1>
<p>The project is licensed under the GPLv2.</p>
</div>
</div>
</body>
</html>
