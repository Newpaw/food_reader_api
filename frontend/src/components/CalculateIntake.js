import React, { useState } from 'react';
import { Formik, Form, Field } from 'formik';
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

const FieldContainer = styled.div`
  margin-bottom: 10px;
`;

const CalculateIntake = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const initialValues = {
    user_id: '',
    height_cm: '',
    weight_kg: '',
    age: '',
    gender: '',
    activity_level: ''
  };

  const handleSubmit = async (values, { setSubmitting }) => {
    setLoading(true);
    try {
      const response = await axiosInstance.post('/calculate-intake', values);
      setResult(response.data);
    } catch (error) {
      alert('Error');
    }
    setLoading(false);
    setSubmitting(false);
  };

  return (
    <Container>
      <h1>Calculate Intake</h1>
      <Formik initialValues={initialValues} onSubmit={handleSubmit}>
        {({ isSubmitting }) => (
          <Form>
            <FieldContainer>
              <Field type="number" name="user_id" placeholder="User ID" />
            </FieldContainer>
            <FieldContainer>
              <Field type="number" name="age" placeholder="Age" />
            </FieldContainer>
            <FieldContainer>
              <Field type="number" name="height_cm" placeholder="Height (cm)" />
            </FieldContainer>
            <FieldContainer>
              <Field type="number" name="weight_kg" placeholder="Weight (kg)" />
            </FieldContainer>
            <FieldContainer>
              <Field as="select" name="gender">
                <option value="" label="Select gender" />
                <option value="male" label="Male" />
                <option value="female" label="Female" />
              </Field>
            </FieldContainer>
            <FieldContainer>
              <Field as="select" name="activity_level">
                <option value="" label="Select activity level" />
                <option value="low" label="Low" />
                <option value="medium" label="Medium" />
                <option value="high" label="High" />
              </Field>
            </FieldContainer>
            <Button type="submit" disabled={isSubmitting || loading}>Calculate</Button>
            {loading && <ClipLoader size={50} color={"#4CAF50"} loading={loading} />}
          </Form>
        )}
      </Formik>
      {result && (
        <div>
          <h2>Daily Intake</h2>
          <p><strong>Calories:</strong> {result.calories}</p>
          <p><strong>Protein (g):</strong> {result.protein_g}</p>
          <p><strong>Fat (g):</strong> {result.fat_g}</p>
          <p><strong>Sugar (g):</strong> {result.sugar_g}</p>
        </div>
      )}
    </Container>
  );
};

export default CalculateIntake;
