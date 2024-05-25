import React, { useState } from 'react';
import { Formik, Form, Field } from 'formik';
import { PacmanLoader } from 'react-spinners';
import axiosInstance from '../axiosConfig';

const CalculateIntake = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const initialValues = {
    user_id: '',
    height_cm: '',
    weight_kg: '',
    age: '',
    gender: '',
    activity_level: '',
  };

  const handleSubmit = async (values, { setSubmitting }) => {
    setLoading(true);
    try {
      const response = await axiosInstance.post('/api/calculate-intake', values);
      setResult(response.data);
    } catch (error) {
      alert('Error');
    }
    setLoading(false);
    setSubmitting(false);
  };

  return (
    <div className="flex flex-col items-center mt-12">
      <h1 className="text-xl font-bold text-center text-gray-800 mt-8 mb-4">Calculate Intake</h1>
      
      <Formik initialValues={initialValues} onSubmit={handleSubmit}>
        {({ isSubmitting }) => (
          <Form>
            <div className="mb-5">
              <Field
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="number"
                name="user_id"
                placeholder="User ID"
              />
            </div>
            <div className="mb-5">
              <Field
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="number"
                name="age"
                placeholder="Age"
              />
            </div>
            <div className="mb-5">
              <Field
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="number"
                name="height_cm"
                placeholder="Height (cm)"
              />
            </div>
            <div className="mb-5">
              <Field
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="number"
                name="weight_kg"
                placeholder="Weight (kg)"
              />
            </div>
            <div className="mb-5">
              <Field
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                as="select"
                name="gender"
              >
                <option value="" label="Select gender" />
                <option value="male" label="Male" />
                <option value="female" label="Female" />
              </Field>
            </div>
            <div className="mb-5">
              <Field
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                as="select"
                name="activity_level"
              >
                <option value="" label="Select activity level" />
                <option value="low" label="Low" />
                <option value="medium" label="Medium" />
                <option value="high" label="High" />
              </Field>
            </div>

            <button
              type="submit"
              disabled={isSubmitting || loading}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Calculate
            </button>

            {loading && (
              <div className="mt-5">
                <PacmanLoader size={50} color={'#4CAF50'} loading={loading} />
              </div>
            )}
          </Form>
        )}
      </Formik>
      {result && (
        <div className="mb-5">
          <h2>Daily Intake</h2>
          <p><strong>Calories:</strong> {result.calories}</p>
          <p><strong>Protein (g):</strong> {result.protein_g}</p>
          <p><strong>Fat (g):</strong> {result.fat_g}</p>
          <p><strong>Sugar (g):</strong> {result.sugar_g}</p>
        </div>
      )}
    </div>
  );
};

export default CalculateIntake;
