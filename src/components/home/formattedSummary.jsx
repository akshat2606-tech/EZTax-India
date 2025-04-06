import React from "react";

export const FormattedSummary = ({ text }) => {
  const formatText = (rawText) => {
    if (!rawText) return [];

    // Escape HTML special characters to prevent XSS
    let safeText = rawText
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    return safeText.split('\n').map((section, index) => {
      let formattedSection = section;

      // Bold (**text**)
      formattedSection = formattedSection.replace(
        /\*\*(.*?)\*\*/g,
        '<strong>$1</strong>'
      );

      // Italic (***text***)
      formattedSection = formattedSection.replace(
        /\*\*\*(.*?)\*\*\*/g,
        '<em>$1</em>'
      );

      // Superscript
      formattedSection = formattedSection.replace(
        /<sup>(.*?)<\/sup>/g,
        '<sup class="text-xs relative -top-1">$1</sup>'
      );

      // Subscript
      formattedSection = formattedSection.replace(
        /<sub>(.*?)<\/sub>/g,
        '<sub class="text-xs relative -bottom-1">$1</sub>'
      );

      return (
        <p
          key={index}
          className="mb-2 last:mb-0"
          dangerouslySetInnerHTML={{ __html: formattedSection }}
        />
      );
    });
  };

  return (
    <div className="prose prose-sm max-w-none">
      {formatText(text)}
    </div>
  );
};

export default FormattedSummary;
