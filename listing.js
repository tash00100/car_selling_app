import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CarListing = () => {
    const [cars, setCars] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/cars')
            .then(response => setCars(response.data))
            .catch(error => console.error('Error fetching cars:', error));
    }, []);

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-6">Car Listings</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {cars.map(car => (
                    <div key={car.id} className="border rounded-lg p-4 shadow-lg">
                        <img 
                            src={car.image_main} 
                            alt={car.make} 
                            className="w-full h-48 object-cover cursor-pointer" 
                            onClick={() => setSelectedImage(car.image_main)}
                        />
                        <h2 className="text-xl font-semibold mt-2">{car.make} {car.model}</h2>
                        <p className="text-gray-700">Price: ${car.price}</p>
                        <p className="text-sm text-gray-500">Seller: {car.seller}</p>
                        <p className="text-sm text-gray-500">Contact: {car.contact_info}</p>
                        <div className="flex gap-2 mt-2">
                            {car.images.map((img, index) => (
                                <img 
                                    key={index} 
                                    src={img} 
                                    alt={`Car ${index}`} 
                                    className="w-16 h-16 object-cover cursor-pointer border rounded"
                                    onClick={() => setSelectedImage(img)}
                                />
                            ))}
                        </div>
                    </div>
                ))}
            </div>
            {selectedImage && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75">
                    <img src={selectedImage} alt="Selected" className="max-w-full max-h-full" />
                    <button 
                        className="absolute top-4 right-4 bg-white px-4 py-2 rounded-lg shadow" 
                        onClick={() => setSelectedImage(null)}
                    >
                        Close
                    </button>
                </div>
            )}
        </div>
    );
};

export default CarListing;
