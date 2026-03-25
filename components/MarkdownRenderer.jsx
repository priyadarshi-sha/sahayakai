'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

/**
 * MarkdownRenderer Component
 * 
 * Renders markdown content with proper styling for:
 * - Bold text (*bold* or **bold**)
 * - Italic text (*italic* or _italic_)
 * - Lists (ordered and unordered)
 * - Code blocks
 * - Headings
 * - Links
 * - Tables (with remark-gfm)
 * - Strikethrough (with remark-gfm)
 */
const MarkdownRenderer = ({ content }) => {
  if (!content) {
    return <p>No content available</p>;
  }

  return (
    <div className="markdown-content prose prose-sm max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Headings
          h1: ({ children }) => <h1 className="text-2xl font-bold mt-6 mb-3">{children}</h1>,
          h2: ({ children }) => <h2 className="text-xl font-bold mt-5 mb-2">{children}</h2>,
          h3: ({ children }) => <h3 className="text-lg font-bold mt-4 mb-2">{children}</h3>,
          h4: ({ children }) => <h4 className="text-base font-bold mt-3 mb-2">{children}</h4>,
          h5: ({ children }) => <h5 className="text-sm font-bold mt-2 mb-1">{children}</h5>,
          h6: ({ children }) => <h6 className="text-xs font-bold mt-2 mb-1">{children}</h6>,

          // Paragraphs
          p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,

          // Lists
          ul: ({ children }) => (
            <ul className="list-disc list-inside mb-3 ml-4 space-y-1">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside mb-3 ml-4 space-y-1">
              {children}
            </ol>
          ),
          li: ({ children }) => <li className="ml-2">{children}</li>,

          // Code
          code: ({ inline, children }) => {
            if (inline) {
              return (
                <code className="bg-gray-200 px-2 py-1 rounded text-sm font-mono">
                  {children}
                </code>
              );
            }
            return (
              <code className="block bg-gray-800 text-white p-4 rounded-lg mb-3 overflow-x-auto">
                {children}
              </code>
            );
          },
          pre: ({ children }) => <pre className="mb-3">{children}</pre>,

          // Blockquotes
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-gray-300 pl-4 py-2 mb-3 italic text-gray-700">
              {children}
            </blockquote>
          ),

          // Links
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline hover:text-blue-800"
            >
              {children}
            </a>
          ),

          // Tables (with remark-gfm)
          table: ({ children }) => (
            <table className="w-full border-collapse mb-3">
              {children}
            </table>
          ),
          thead: ({ children }) => (
            <thead className="bg-gray-200">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody>
              {children}
            </tbody>
          ),
          tr: ({ children }) => (
            <tr className="border">
              {children}
            </tr>
          ),
          th: ({ children }) => (
            <th className="border px-4 py-2 text-left font-semibold">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border px-4 py-2">
              {children}
            </td>
          ),

          // Horizontal rule
          hr: () => <hr className="my-4 border-gray-300" />,

          // Strong (bold)
          strong: ({ children }) => <strong className="font-bold">{children}</strong>,

          // Emphasis (italic)
          em: ({ children }) => <em className="italic">{children}</em>,

          // Deleted text (strikethrough with remark-gfm)
          del: ({ children }) => <del className="line-through">{children}</del>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
