import React, { useState } from 'react';
import api from '../api'; 
import { useNavigate } from 'react-router-dom';
import '../styles/LostFoundForm.css';

const LostFoundForm = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [status, setStatus] = useState('lost'); 
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(null);

        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description || 'No description provided');

        if (image) {
            formData.append('image', image);
        }

        formData.append('status', status); 

        try {
            const response = await api.post('/api/lost-found/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setSuccess(response.data.message);
            if (status === 'lost') {
                setTimeout(() => {
                    navigate('/found-items'); 
                }, 1000); 
            }
            resetForm();
        } catch (error) {
            console.error(error);
            setError(error.response?.data?.message || 'Failed to post item. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setTitle('');
        setDescription('');
        setImage(null);
        setImagePreview(null);
        setStatus('lost');
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setImagePreview(URL.createObjectURL(file)); 
        }
    };

    return (
        <div className="form-container">
            <h2>Post Lost/Found Item</h2>
            {loading && <p className="loading-indicator">Submitting...</p>}
            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">{success}</p>}
            <form onSubmit={handleSubmit} className="form">
                <div className="form-group">
                    <label htmlFor="title">Title</label>
                    <input
                        type="text"
                        id="title"
                        placeholder="Enter the title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="description">Description</label>
                    <textarea
                        id="description"
                        placeholder="Enter a description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="image">Upload Image</label>
                    <input
                        type="file"
                        id="image"
                        accept="image/*"
                        onChange={handleImageChange}
                    />
                    {imagePreview && <img src={imagePreview} alt="Preview" className="image-preview" />}
                </div>
                <div className="form-group">
                    <label htmlFor="status">Status</label>
                    <select
                        id="status"
                        value={status}
                        onChange={(e) => setStatus(e.target.value)}
                    >
                        <option value="lost">Lost</option>
                        <option value="found">Found</option>
                    </select>
                </div>
                <button type="submit" className="form-button">Submit</button>
            </form>
        </div>
    );
};

export default LostFoundForm;