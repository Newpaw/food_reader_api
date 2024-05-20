import React, { useState } from 'react';
import styled from 'styled-components';
import { ClipLoader } from 'react-spinners';
import axiosInstance from '../axiosConfig';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
`;

const Button = styled.button`
  padding: 10px 20px;
  margin-top: 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

const Input = styled.input`
  margin-top: 20px;
`;

const ResultContainer = styled.div`
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  width: 300px;
  text-align: left;
`;

const ResultItem = styled.div`
  margin-bottom: 10px;
`;

const AnalyzeImage = () => {
  const [file, setFile] = useState(null);
  const [foodInfo, setFoodInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
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
    <Container>
      <h1>Analyze Image</h1>
      <Input type="file" onChange={handleFileChange} />
      <Button onClick={handleSubmit}>Upload</Button>
      {loading ? (
        <ClipLoader size={50} color={"#4CAF50"} loading={loading} />
      ) : (
        foodInfo && (
          <ResultContainer>
            <h2>Analysis Result</h2>
            <ResultItem>
              <strong>Certainty:</strong> {foodInfo.certainty}
            </ResultItem>
            <ResultItem>
              <strong>Food Name:</strong> {foodInfo.food_name}
            </ResultItem>
            <ResultItem>
              <strong>Calories:</strong> {foodInfo.calories_Kcal} Kcal
            </ResultItem>
            <ResultItem>
              <strong>Fat:</strong> {foodInfo.fat_in_g} g
            </ResultItem>
            <ResultItem>
              <strong>Protein:</strong> {foodInfo.protein_in_g} g
            </ResultItem>
            <ResultItem>
              <strong>Sugar:</strong> {foodInfo.sugar_in_g} g
            </ResultItem>
          </ResultContainer>
        )
      )}
    </Container>
  );
};

export default AnalyzeImage;
