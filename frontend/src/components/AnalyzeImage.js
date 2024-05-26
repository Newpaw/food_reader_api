import React, { useState, useRef } from 'react';
import { PacmanLoader } from 'react-spinners';
import axiosInstance from '../axiosConfig';

const AnalyzeImage = () => {
  const [file, setFile] = useState(null);
  const [foodInfo, setFoodInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);

    try {
      const response = await axiosInstance.post('/api/analyze-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setFoodInfo(response.data);
    } catch (error) {
      alert('Error analyzing image. Catch error: ' + error.message);
      console.error('Error analyzing image:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center mt-12">
      <h1 className="text-2xl font-bold">Analyze Image</h1>
      <input
        type="file"
        onChange={handleFileChange}
        accept="image/*"
        capture="environment"
        className="hidden"
        ref={fileInputRef}
      />
      <div className="mt-5 flex items-center">
        <button
          onClick={handleButtonClick}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          {file ? 'Change Image' : 'Choose an Image'}
        </button>
        {file && (
          <img
            src={URL.createObjectURL(file)}
            alt="Thumbnail"
            className="ml-4 w-16 h-16 object-cover rounded"
          />
        )}
      </div>
      {file && (
        <button
          onClick={handleSubmit}
          className="mt-5 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
        >
          Upload
        </button>
      )}
      {loading ? (
        <div className="mt-5">
          <PacmanLoader size={50} color={"#4CAF50"} loading={loading} />
        </div>
      ) : (
        foodInfo && (
          <div className="mt-5 p-5 border border-gray-300 rounded bg-gray-100 w-72 text-left">
            <h2 className="text-xl font-semibold">Analysis Result</h2>
            <div className="mt-2">
              <strong>Certainty:</strong> {foodInfo.certainty}
            </div>
            <div className="mt-2">
              <strong>Food Name:</strong> {foodInfo.food_name}
            </div>
            <div className="mt-2">
              <strong>Calories:</strong> {foodInfo.calories_Kcal} Kcal
            </div>
            <div className="mt-2">
              <strong>Fat:</strong> {foodInfo.fat_in_g} g
            </div>
            <div className="mt-2">
              <strong>Protein:</strong> {foodInfo.protein_in_g} g
            </div>
            <div className="mt-2">
              <strong>Sugar:</strong> {foodInfo.sugar_in_g} g
            </div>
          </div>
        )
      )}
    </div>
  );
};

export default AnalyzeImage;
