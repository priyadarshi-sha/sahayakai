import React from "react";

const YoutubeCard = ({ title, id, index }) => {
  const thumbnail = `https://img.youtube.com/vi/${id}/0.jpg`;

  return (
    <a
      href={`https://www.youtube.com/watch?v=${id}`}
      target="_blank"
      rel="noopener noreferrer"
      className="relative w-[250px] cursor-pointer"
    >
      <div className="relative overflow-hidden rounded-xl shadow-md">

        {/* Thumbnail */}
        <img
          src={thumbnail}
          alt={title}
          className="w-full h-[150px] object-cover opacity-70 hover:opacity-100 transition duration-300"
        />

        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-black opacity-30 hover:opacity-10 transition duration-300"></div>

        {/* Play Button */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="bg-red-600 rounded-full p-3 shadow-lg">
            ▶
          </div>
        </div>
      </div>

      {/* Title */}
      <p className="mt-2 text-sm font-medium line-clamp-2">
        {title}
      </p>
    </a>
  );
};

export default YoutubeCard;
