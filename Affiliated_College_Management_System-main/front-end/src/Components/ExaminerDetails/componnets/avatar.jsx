import React from "react";

const Avatar = ({ src, name }) => {
  return (
    <div className="bg-white w-full p-md-5 p-2 card">
      <img
        src={src ?? "/user-placeholder.jpg"}
        alt={name}
        width={200}
        height={200}
        className="text-center mx-auto rounded-circle image-avatar"
        // style={{ width: "200px", height: "200px" }}
      ></img>
      <h4 className="heading-4 text-center mt-4">{name}</h4>
    </div>
  );
};

export default Avatar;
