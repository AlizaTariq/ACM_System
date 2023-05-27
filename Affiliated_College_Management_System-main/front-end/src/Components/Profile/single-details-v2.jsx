import React from "react";

const SingleDetailsV2 = ({ heading, text, file }) => {
  return (
    <div className="py-3">
      <h4 className="heading-4 text-left mb-2">{heading}</h4>
      {file ? (
        <a href="/assets/pdf/abc.pdf" download>
          Click here download
        </a>
      ) : (
        <h4 className="heading-6 text-left text-secondary">{text}</h4>
      )}
    </div>
  );
};

export default SingleDetailsV2;
