from flask import Flask, request, render_template, redirect, url_for, session, jsonify, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import os
import requests
import json
import datetime
import random
import math
import string
import logging
import io
import csv
from flask import session

NCERT_QUESTION_BANK = {
    '8th': [
        {
            'question_en': 'What is the sum of the angles in a triangle?',
            'question_hi': 'त्रिभुज के कोणों का योगफल कितना होता है?',
            'question_kn': 'ತ್ರಿಭುಜದ ಆಂಗಲಗಳ ಮೊತ್ತ ಎಷ್ಟು?',
            'options_en': ['90°', '180°', '360°', '120°'],
            'options_hi': ['90°', '180°', '360°', '120°'],
            'options_kn': ['90°', '180°', '360°', '120°'],
            'correct_answer': '180°',
            'explanation_en': 'The sum of the interior angles of a triangle is always 180 degrees.',
            'explanation_hi': 'त्रिभुज के आंतरिक कोणों का योग हमेशा 180 डिग्री होता है।',
            'explanation_kn': 'ತ್ರಿಭುಜದ ಆಂತರಿಕ ಆಂಗಲಗಳ ಮೊತ್ತ ಯಾವಾಗಲೂ 180 ಡಿಗ್ರಿ ಆಗಿರುತ್ತದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'Simplify: 2 + 3 × 4',
            'question_hi': 'सरल कीजिए: 2 + 3 × 4',
            'question_kn': 'ಸರಳಗೊಳಿಸಿ: 2 + 3 × 4',
            'options_en': ['20', '14', '10', '12'],
            'options_hi': ['20', '14', '10', '12'],
            'options_kn': ['20', '14', '10', '12'],
            'correct_answer': '14',
            'explanation_en': 'Using BODMAS, first calculate 3 × 4 = 12, then add 2 to get 14.',
            'explanation_hi': 'BODMAS के अनुसार, पहले 3 × 4 = 12 फिर 2 जोड़कर 14 प्राप्त होता है।',
            'explanation_kn': 'BODMAS ಅನ್ನು ಬಳಸಿದರೆ, ಮೊದಲು 3 × 4 = 12, ನಂತರ 2 ಸೇರಿಸಿ 14 ಆಗುತ್ತದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Basic Arithmetic'
        },
        {
            'question_en': 'What is the value of 5²?',
            'question_hi': '5² का मान क्या है?',
            'question_kn': '5² ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['10', '15', '25', '20'],
            'options_hi': ['10', '15', '25', '20'],
            'options_kn': ['10', '15', '25', '20'],
            'correct_answer': '25',
            'explanation_en': '5² means 5 × 5 = 25.',
            'explanation_hi': '5² का अर्थ 5 × 5 = 25 है।',
            'explanation_kn': '5² ಎಂದರೆ 5 × 5 = 25.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Squares and Square Roots'
        },
        {
            'question_en': 'Find the perimeter of a square with side length 4 cm.',
            'question_hi': '4 सेमी भुजा वाले वर्ग का परिमाप ज्ञात कीजिए।',
            'question_kn': '4 ಸೆಂ.ಮೀ ಭುಜದ ಚೌಕದ ಪರಿಮಿತಿಯನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ.',
            'options_en': ['12 cm', '16 cm', '8 cm', '20 cm'],
            'options_hi': ['12 सेमी', '16 सेमी', '8 सेमी', '20 सेमी'],
            'options_kn': ['12 ಸೆಂ.ಮೀ', '16 ಸೆಂ.ಮೀ', '8 ಸೆಂ.ಮೀ', '20 ಸೆಂ.ಮೀ'],
            'correct_answer': '16 cm',
            'explanation_en': 'Perimeter of a square = 4 × side = 4 × 4 = 16 cm.',
            'explanation_hi': 'वर्ग का परिमाप = 4 × भुजा = 4 × 4 = 16 सेमी।',
            'explanation_kn': 'ಚೌಕದ ಪರಿಮಿತಿ = 4 × ಭುಜ = 4 × 4 = 16 ಸೆಂ.ಮೀ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Mensuration'
        },
        {
            'question_en': 'Which of the following is a right-angled triangle?',
            'question_hi': 'निम्नलिखित में से कौन सा समकोण त्रिभुज है?',
            'question_kn': 'ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು ಲಂಬಕೋನ ತ್ರಿಭುಜ?',
            'options_en': ['30°, 60°, 90°', '60°, 60°, 60°', '90°, 45°, 45°', '120°, 30°, 30°'],
            'options_hi': ['30°, 60°, 90°', '60°, 60°, 60°', '90°, 45°, 45°', '120°, 30°, 30°'],
            'options_kn': ['30°, 60°, 90°', '60°, 60°, 60°', '90°, 45°, 45°', '120°, 30°, 30°'],
            'correct_answer': '30°, 60°, 90°',
            'explanation_en': 'A right angle is 90°, so 30°, 60°, 90° is right-angled.',
            'explanation_hi': 'समकोण 90° होता है, इसलिए 30°, 60°, 90° समकोण त्रिभुज है।',
            'explanation_kn': 'ಲಂಬಕೋನವು 90° ಆಗಿರುತ್ತದೆ, ಆದ್ದರಿಂದ 30°, 60°, 90° ಲಂಬಕೋನ ತ್ರಿಭುಜವಾಗಿದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'What is 7 × 6?',
            'question_hi': '7 × 6 का मान क्या है?',
            'question_kn': '7 × 6 ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['42', '36', '48', '40'],
            'options_hi': ['42', '36', '48', '40'],
            'options_kn': ['42', '36', '48', '40'],
            'correct_answer': '42',
            'explanation_en': 'Multiplication of 7 and 6 is 42.',
            'explanation_hi': '7 और 6 का गुणनफल 42 है।',
            'explanation_kn': '7 ಮತ್ತು 6 ರ ಗುಣಾಕಾರ 42 ಆಗಿದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Basic Arithmetic'
        },
        {
            'question_en': 'Which shape has all sides equal and angles 90°?',
            'question_hi': 'कौन सा आकार सभी भुजाएँ समान और कोण 90° वाला है?',
            'question_kn': 'ಯಾವ ಆಕಾರವು ಎಲ್ಲಾ ಭುಜಗಳು ಸಮಾನ ಮತ್ತು 90° ಕೋನಗಳನ್ನು ಹೊಂದಿದೆ?',
            'options_en': ['Rectangle', 'Rhombus', 'Square', 'Trapezium'],
            'options_hi': ['आयत', 'समचतुर्भुज', 'वर्ग', 'समलंब'],
            'options_kn': ['ಆಯತ', 'ರಾಂಬಸ್', 'ಚೌಕ', 'ಟ್ರಾಪಿಜಿಯಮ್'],
            'correct_answer': 'Square',
            'explanation_en': 'A square has all equal sides and 90° angles.',
            'explanation_hi': 'वर्ग की सभी भुजाएँ समान और कोण 90° होते हैं।',
            'explanation_kn': 'ಚೌಕವು ಎಲ್ಲಾ ಸಮಾನ ಭುಜಗಳನ್ನು ಮತ್ತು 90° ಕೋನಗಳನ್ನು ಹೊಂದಿದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Mensuration'
        },
        {
            'question_en': 'What is the square root of 49?',
            'question_hi': '49 का वर्गमूल क्या है?',
            'question_kn': '49 ರ ವರ್ಗಮೂಲ ಎಷ್ಟು?',
            'options_en': ['5', '6', '7', '8'],
            'options_hi': ['5', '6', '7', '8'],
            'options_kn': ['5', '6', '7', '8'],
            'correct_answer': '7',
            'explanation_en': '7 × 7 = 49, so √49 = 7.',
            'explanation_hi': '7 × 7 = 49, इसलिए √49 = 7।',
            'explanation_kn': '7 × 7 = 49, ಆದ್ದರಿಂದ √49 = 7.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Squares and Square Roots'
        },
        {
            'question_en': 'Area of square with side 5 cm?',
            'question_hi': '5 सेमी भुजा वाले वर्ग का क्षेत्रफल?',
            'question_kn': '5 ಸೆಂ.ಮೀ ಭುಜದ ಚೌಕದ ವಿಸ್ತೀರ್ಣ?',
            'options_en': ['10 cm²', '25 cm²', '15 cm²', '20 cm²'],
            'options_hi': ['10 सेमी²', '25 सेमी²', '15 सेमी²', '20 सेमी²'],
            'options_kn': ['10 ಸೆಂ.ಮೀ²', '25 ಸೆಂ.ಮೀ²', '15 ಸೆಂ.ಮೀ²', '20 ಸೆಂ.ಮೀ²'],
            'correct_answer': '25 cm²',
            'explanation_en': 'Area = side² = 5² = 25 cm².',
            'explanation_hi': 'क्षेत्रफल = भुजा² = 5² = 25 सेमी²।',
            'explanation_kn': 'ವಿಸ್ತೀರ್ಣ = ಭುಜ² = 5² = 25 ಸೆಂ.ಮೀ².',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Mensuration'
        },
        {
            'question_en': 'What is the value of 3² + 4²?',
            'question_hi': '3² + 4² का मान क्या है?',
            'question_kn': '3² + 4² ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['12', '25', '5', '7'],
            'options_hi': ['12', '25', '5', '7'],
            'options_kn': ['12', '25', '5', '7'],
            'correct_answer': '25',
            'explanation_en': '3² + 4² = 9 + 16 = 25.',
            'explanation_hi': '3² + 4² = 9 + 16 = 25।',
            'explanation_kn': '3² + 4² = 9 + 16 = 25.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Squares and Square Roots'
        },
        {
            'question_en': 'How many sides does a triangle have?',
            'question_hi': 'त्रिभुज की कितनी भुजाएँ होती हैं?',
            'question_kn': 'ತ್ರಿಭುಜವು ಎಷ್ಟು ಭುಜಗಳನ್ನು ಹೊಂದಿದೆ?',
            'options_en': ['2', '3', '4', '5'],
            'options_hi': ['2', '3', '4', '5'],
            'options_kn': ['2', '3', '4', '5'],
            'correct_answer': '3',
            'explanation_en': 'By definition, a triangle has 3 sides.',
            'explanation_hi': 'परिभाषा के अनुसार, त्रिभुज की 3 भुजाएँ होती हैं।',
            'explanation_kn': 'ವ್ಯಾಖ್ಯಾನದಿಂದ, ತ್ರಿಭುಜವು 3 ಭುಜಗಳನ್ನು ಹೊಂದಿದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'Simplify: 12 ÷ 3 + 2',
            'question_hi': 'सरल कीजिए: 12 ÷ 3 + 2',
            'question_kn': 'ಸರಳಗೊಳಿಸಿ: 12 ÷ 3 + 2',
            'options_en': ['2', '4', '6', '8'],
            'options_hi': ['2', '4', '6', '8'],
            'options_kn': ['2', '4', '6', '8'],
            'correct_answer': '6',
            'explanation_en': '12 ÷ 3 = 4, then 4 + 2 = 6.',
            'explanation_hi': '12 ÷ 3 = 4, फिर 4 + 2 = 6।',
            'explanation_kn': '12 ÷ 3 = 4, ನಂತರ 4 + 2 = 6.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Basic Arithmetic'
        },
        {
            'question_en': 'Volume of a cube with side 3 cm?',
            'question_hi': '3 सेमी भुजा वाले घन का आयतन?',
            'question_kn': '3 ಸೆಂ.ಮೀ ಭುಜದ ಘನದ ಘನಫಲ?',
            'options_en': ['27 cm³', '9 cm³', '18 cm³', '36 cm³'],
            'options_hi': ['27 सेमी³', '9 सेमी³', '18 सेमी³', '36 सेमी³'],
            'options_kn': ['27 ಸೆಂ.ಮೀ³', '9 ಸೆಂ.ಮೀ³', '18 ಸೆಂ.ಮೀ³', '36 ಸೆಂ.ಮೀ³'],
            'correct_answer': '27 cm³',
            'explanation_en': 'Volume = side³ = 3³ = 27 cm³.',
            'explanation_hi': 'आयतन = भुजा³ = 3³ = 27 सेमी³।',
            'explanation_kn': 'ಘನಫಲ = ಭುಜ³ = 3³ = 27 ಸೆಂ.ಮೀ³.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Mensuration'
        },
        {
            'question_en': 'What is the square of 11?',
            'question_hi': '11 का वर्ग क्या है?',
            'question_kn': '11 ರ ವರ್ಗ ಎಷ್ಟು?',
            'options_en': ['121', '111', '110', '100'],
            'options_hi': ['121', '111', '110', '100'],
            'options_kn': ['121', '111', '110', '100'],
            'correct_answer': '121',
            'explanation_en': '11² = 121.',
            'explanation_hi': '11² = 121।',
            'explanation_kn': '11² = 121.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Squares and Square Roots'
        },
        {
            'question_en': 'Triangle with all sides equal is called?',
            'question_hi': 'सभी भुजाएँ समान वाला त्रिभुज क्या कहलाता है?',
            'question_kn': 'ಎಲ್ಲಾ ಭುಜಗಳು ಸಮಾನವಾಗಿರುವ ತ್ರಿಭುಜವನ್ನು ಏನೆಂದು ಕರೆಯಲಾಗುತ್ತದೆ?',
            'options_en': ['Isosceles', 'Scalene', 'Equilateral', 'Right-Angled'],
            'options_hi': ['समद्विबाहु', 'विषमबाहु', 'समबाहु', 'समकोण'],
            'options_kn': ['ಐಸಾಸೆಲೀಸ್', 'ಸ್ಕೇಲೀನ್', 'ಸಮಬಾಹು', 'ಲಂಬಕೋನ'],
            'correct_answer': 'Equilateral',
            'explanation_en': 'An equilateral triangle has all sides equal.',
            'explanation_hi': 'समबाहु त्रिभुज की सभी भुजाएँ समान होती हैं।',
            'explanation_kn': 'ಸಮಬಾಹು ತ್ರಿಭುಜವು ಎಲ್ಲಾ ಭುಜಗಳು ಸಮಾನವಾಗಿರುತ್ತದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'Which operation comes first in BODMAS?',
            'question_hi': 'BODMAS में कौन सा ऑपरेशन पहले आता है?',
            'question_kn': 'BODMAS ನಲ್ಲಿ ಯಾವ ಕಾರ್ಯಾಚರಣೆ ಮೊದಲು ಬರುತ್ತದೆ?',
            'options_en': ['Addition', 'Division', 'Brackets', 'Multiplication'],
            'options_hi': ['जोड़', 'भाग', 'कोष्ठक', 'गुणा'],
            'options_kn': ['ಕೂಡುವಿಕೆ', 'ಭಾಗಾಕಾರ', 'ಕೋಷ್ಟಕಗಳು', 'ಗುಣಾಕಾರ'],
            'correct_answer': 'Brackets',
            'explanation_en': 'BODMAS stands for Brackets, Orders, Division, Multiplication, Addition, Subtraction.',
            'explanation_hi': 'BODMAS का अर्थ है कोष्ठक, घात, भाग, गुणा, जोड़, घटाव।',
            'explanation_kn': 'BODMAS ಎಂದರೆ ಕೋಷ್ಟಕಗಳು, ಘಾತಗಳು, ಭಾಗಾಕಾರ, ಗುಣಾಕಾರ, ಕೂಡುವಿಕೆ, ಕಳೆಯುವಿಕೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Basic Arithmetic'
        },
        {
            'question_en': 'Which unit is used to measure area?',
            'question_hi': 'क्षेत्रफल मापने के लिए कौन सी इकाई उपयोग की जाती है?',
            'question_kn': 'ವಿಸ್ತೀರ್ಣವನ್ನು ಅಳೆಯಲು ಯಾವ ಘಟಕವನ್ನು ಬಳಸಲಾಗುತ್ತದೆ?',
            'options_en': ['cm', 'cm²', 'cm³', 'cm/s'],
            'options_hi': ['सेमी', 'सेमी²', 'सेमी³', 'सेमी/सेकंड'],
            'options_kn': ['ಸೆಂ.ಮೀ', 'ಸೆಂ.ಮೀ²', 'ಸೆಂ.ಮೀ³', 'ಸೆಂ.ಮೀ/ಸೆಕೆಂಡ್'],
            'correct_answer': 'cm²',
            'explanation_en': 'Area is measured in square units like cm².',
            'explanation_hi': 'क्षेत्रफल वर्ग इकाइयों में मापा जाता है जैसे सेमी²।',
            'explanation_kn': 'ವಿಸ್ತೀರ್ಣವನ್ನು ಸೆಂ.ಮೀ² ನಂತಹ ಚದರ ಘಟಕಗಳಲ್ಲಿ ಅಳೆಯಲಾಗುತ್ತದೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Mensuration'
        },
        {
            'question_en': 'What is 10²?',
            'question_hi': '10² का मान क्या है?',
            'question_kn': '10² ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['20', '100', '50', '10'],
            'options_hi': ['20', '100', '50', '10'],
            'options_kn': ['20', '100', '50', '10'],
            'correct_answer': '100',
            'explanation_en': '10² = 10 × 10 = 100.',
            'explanation_hi': '10² = 10 × 10 = 100।',
            'explanation_kn': '10² = 10 × 10 = 100.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Squares and Square Roots'
        },
        {
            'question_en': 'What is the area of a triangle with base 6 cm and height 2 cm?',
            'question_hi': '6 सेमी आधार और 2 सेमी ऊँचाई वाले त्रिभुज का क्षेत्रफल क्या है?',
            'question_kn': '6 ಸೆಂ.ಮೀ ಆಧಾರ ಮತ್ತು 2 ಸೆಂ.ಮೀ ಎತ್ತರದ ತ್ರಿಭುಜದ ವಿಸ್ತೀರ್ಣ ಎಷ್ಟು?',
            'options_en': ['6 cm²', '8 cm²', '12 cm²', '10 cm²'],
            'options_hi': ['6 सेमी²', '8 सेमी²', '12 सेमी²', '10 सेमी²'],
            'options_kn': ['6 ಸೆಂ.ಮೀ²', '8 ಸೆಂ.ಮೀ²', '12 ಸೆಂ.ಮೀ²', '10 ಸೆಂ.ಮೀ²'],
            'correct_answer': '6 cm²',
            'explanation_en': 'Area = ½ × base × height = ½ × 6 × 2 = 6 cm².',
            'explanation_hi': 'क्षेत्रफल = ½ × आधार × ऊँचाई = ½ × 6 × 2 = 6 सेमी²।',
            'explanation_kn': 'ವಿಸ್ತೀರ್ಣ = ½ × ಆಧಾರ × ಎತ್ತರ = ½ × 6 × 2 = 6 ಸೆಂ.ಮೀ².',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Mensuration'
        },
        {
            'question_en': 'Which triangle has no equal sides?',
            'question_hi': 'कौन सा त्रिभुज की कोई भी भुजाएँ समान नहीं हैं?',
            'question_kn': 'ಯಾವ ತ್ರಿಭುಜವು ಯಾವುದೇ ಸಮಾನ ಭುಜಗಳನ್ನು ಹೊಂದಿಲ್ಲ?',
            'options_en': ['Isosceles', 'Equilateral', 'Right-Angled', 'Scalene'],
            'options_hi': ['समद्विबाहु', 'समबाहु', 'समकोण', 'विषमबाहु'],
            'options_kn': ['ಐಸಾಸೆಲೀಸ್', 'ಸಮಬಾಹು', 'ಲಂಬಕೋನ', 'ಸ್ಕೇಲೀನ್'],
            'correct_answer': 'Scalene',
            'explanation_en': 'A scalene triangle has all sides different.',
            'explanation_hi': 'विषमबाहु त्रिभुज की सभी भुजाएँ भिन्न होती हैं।',
            'explanation_kn': 'ಸ್ಕೇಲೀನ್ ತ್ರಿಭುಜವು ಎಲ್ಲಾ ಭುಜಗಳು ಭಿನ್ನವಾಗಿರುತ್ತವೆ.',
            'type': 'Math_8th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        }
    ],
    '9th': [
        {
            'question_en': 'What is the degree of the polynomial 3x² + 2x + 1?',
            'question_hi': '3x² + 2x + 1 बहुपद की डिग्री क्या है?',
            'question_kn': '3x² + 2x + 1 ಬಹುಪದದ ಡಿಗ್ರಿ ಎಷ್ಟು?',
            'options_en': ['1', '2', '3', '0'],
            'options_hi': ['1', '2', '3', '0'],
            'options_kn': ['1', '2', '3', '0'],
            'correct_answer': '2',
            'explanation_en': 'The degree of a polynomial is the highest power of x, which is 2 here.',
            'explanation_hi': 'बहुपद की डिग्री x की सबसे उच्च घात है, जो यहाँ 2 है।',
            'explanation_kn': 'ಬಹುಪದದ ಡಿಗ್ರಿಯು x ನ ಅತಿ ಹೆಚ್ಚಿನ ಘಾತವಾಗಿದೆ, ಇಲ್ಲಿ ಇದು 2 ಆಗಿದೆ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'If two angles of a triangle are 40° and 70°, what is the third angle?',
            'question_hi': 'यदि त्रिभुज के दो कोण 40° और 70° हैं, तो तीसरा कोण क्या है?',
            'question_kn': 'ತ್ರಿಭುಜದ ಎರಡು ಕೋನಗಳು 40° ಮತ್ತು 70° ಆಗಿದ್ದರೆ, ಮೂರನೇ ಕೋನ ಎಷ್ಟು?',
            'options_en': ['60°', '70°', '80°', '90°'],
            'options_hi': ['60°', '70°', '80°', '90°'],
            'options_kn': ['60°', '70°', '80°', '90°'],
            'correct_answer': '70°',
            'explanation_en': 'Sum of angles in a triangle = 180°. Third angle = 180° - 40° - 70° = 70°.',
            'explanation_hi': 'त्रिभुज के कोणों का योग = 180°। तीसरा कोण = 180° - 40° - 70° = 70°।',
            'explanation_kn': 'ತ್ರಿಭುಜದ ಕೋನಗಳ ಮೊತ್ತ = 180°. ಮೂರನೇ ಕೋನ = 180° - 40° - 70° = 70°.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'What is the value of √16?',
            'question_hi': '√16 का मान क्या है?',
            'question_kn': '√16 ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['2', '4', '8', '16'],
            'options_hi': ['2', '4', '8', '16'],
            'options_kn': ['2', '4', '8', '16'],
            'correct_answer': '4',
            'explanation_en': 'The square root of 16 is 4, since 4 × 4 = 16.',
            'explanation_hi': '16 का वर्गमूल 4 है, क्योंकि 4 × 4 = 16।',
            'explanation_kn': '16 ರ ವರ್ಗಮೂಲ 4 ಆಗಿದೆ, ಏಕೆಂದರೆ 4 × 4 = 16.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        },
        {
            'question_en': 'What is the HCF of 12 and 18?',
            'question_hi': '12 और 18 का HCF क्या है?',
            'question_kn': '12 ಮತ್ತು 18 ರ HCF ಎಷ್ಟು?',
            'options_en': ['3', '6', '9', '12'],
            'options_hi': ['3', '6', '9', '12'],
            'options_kn': ['3', '6', '9', '12'],
            'correct_answer': '6',
            'explanation_en': 'HCF of 12 and 18 = 2 × 3 = 6 using prime factorization.',
            'explanation_hi': '12 और 18 का HCF = 2 × 3 = 6, अभाज्य गुणनखंडन द्वारा।',
            'explanation_kn': '12 ಮತ್ತು 18 ರ HCF = 2 × 3 = 6, ಮೊದಲ ಗುಣಾಕಾರದಿಂದ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        },
        {
            'question_en': 'What type of triangle has sides 5 cm, 5 cm, and 6 cm?',
            'question_hi': '5 सेमी, 5 सेमी, और 6 सेमी भुजाओं वाला त्रिभुज किस प्रकार का है?',
            'question_kn': '5 ಸೆಂ.ಮೀ, 5 ಸೆಂ.ಮೀ, ಮತ್ತು 6 ಸೆಂ.ಮೀ ಭುಜಗಳ ತ್ರಿಭುಜ ಯಾವ ಪ್ರಕಾರದ್ದು?',
            'options_en': ['Equilateral', 'Scalene', 'Isosceles', 'Right'],
            'options_hi': ['समबाहु', 'विषमबाहु', 'समद्विबाहु', 'समकोण'],
            'options_kn': ['ಸಮಬಾಹು', 'ಸ್ಕೇಲೀನ್', 'ಐಸಾಸೆಲೀಸ್', 'ಲಂಬಕೋನ'],
            'correct_answer': 'Isosceles',
            'explanation_en': 'Two sides are equal, so it is an isosceles triangle.',
            'explanation_hi': 'दो भुजाएँ समान हैं, इसलिए यह समद्विबाहु त्रिभुज है।',
            'explanation_kn': 'ಎರಡು ಭುಜಗಳು ಸಮಾನವಾಗಿವೆ, ಆದ್ದರಿಂದ ಇದು ಐಸಾಸೆಲೀಸ್ ತ್ರಿಭುಜವಾಗಿದೆ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'Is √2 a rational number?',
            'question_hi': 'क्या √2 एक परिमेय संख्या है?',
            'question_kn': '√2 ಒಂದು ಭಿನ್ನರಾಶಿಯ ಸಂಖ್ಯೆಯೇ?',
            'options_en': ['Yes', 'No', 'Only when squared', 'Sometimes'],
            'options_hi': ['हाँ', 'नहीं', 'केवल वर्ग करने पर', 'कभी-कभी'],
            'options_kn': ['ಹೌದು', 'ಇಲ್ಲ', 'ಕೇವಲ ವರ್ಗ ಮಾಡಿದಾಗ', 'ಕೆಲವೊಮ್ಮೆ'],
            'correct_answer': 'No',
            'explanation_en': '√2 is irrational as it cannot be expressed as a fraction.',
            'explanation_hi': '√2 अपरिमेय है क्योंकि इसे भिन्न के रूप में व्यक्त नहीं किया जा सकता।',
            'explanation_kn': '√2 ಅಪರಿಮಿತವಾಗಿದೆ ಏಕೆಂದರೆ ಇದನ್ನು ಭಿನ್ನರಾಶಿಯಾಗಿ ವ್ಯಕ್ತಪಡಿಸಲಾಗದು.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        },
        {
            'question_en': 'Factor: x² - 9',
            'question_hi': 'गुणनखंड कीजिए: x² - 9',
            'question_kn': 'ಗುಣಾಕಾರ ಮಾಡಿ: x² - 9',
            'options_en': ['(x + 3)(x - 3)', '(x - 9)(x + 1)', '(x - 3)²', '(x - 9)(x - 1)'],
            'options_hi': ['(x + 3)(x - 3)', '(x - 9)(x + 1)', '(x - 3)²', '(x - 9)(x - 1)'],
            'options_kn': ['(x + 3)(x - 3)', '(x - 9)(x + 1)', '(x - 3)²', '(x - 9)(x - 1)'],
            'correct_answer': '(x + 3)(x - 3)',
            'explanation_en': 'This is a difference of squares: a² - b² = (a + b)(a - b).',
            'explanation_hi': 'यह वर्गों का अंतर है: a² - b² = (a + b)(a - b)।',
            'explanation_kn': 'ಇದು ಚದರಗಳ ವ್ಯತ್ಯಾಸವಾಗಿದೆ: a² - b² = (a + b)(a - b).',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'A triangle with all unequal sides is called?',
            'question_hi': 'सभी असमान भुजाओं वाला त्रिभुज क्या कहलाता है?',
            'question_kn': 'ಎಲ್ಲಾ ಅಸಮಾನ ಭುಜಗಳ ತ್ರಿಭುಜವನ್ನು ಏನೆಂದು ಕರೆಯಲಾಗುತ್ತದೆ?',
            'options_en': ['Isosceles', 'Equilateral', 'Scalene', 'Right'],
            'options_hi': ['समद्विबाहु', 'समबाहु', 'विषमबाहु', 'समकोण'],
            'options_kn': ['ಐಸಾಸೆಲೀಸ್', 'ಸಮಬಾಹು', 'ಸ್ಕೇಲೀನ್', 'ಲಂಬಕೋನ'],
            'correct_answer': 'Scalene',
            'explanation_en': 'Scalene triangles have no equal sides.',
            'explanation_hi': 'विषमबाहु त्रिभुज की कोई भी भुजाएँ समान नहीं होतीं।',
            'explanation_kn': 'ಸ್ಕೇಲೀನ್ ತ್ರಿಭುಜಗಳು ಯಾವುದೇ ಸಮಾನ ಭುಜಗಳನ್ನು ಹೊಂದಿರುವುದಿಲ್ಲ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'Which number is both rational and a whole number?',
            'question_hi': 'कौन सी संख्या परिमेय और पूर्ण संख्या दोनों है?',
            'question_kn': 'ಯಾವ ಸಂಖ್ಯೆಯು ಭಿನ್ನರಾಶಿಯ ಮತ್ತು ಪೂರ್ಣ ಸಂಖ್ಯೆ ಎರಡೂ ಆಗಿದೆ?',
            'options_en': ['0', '√2', '1.5', '3/4'],
            'options_hi': ['0', '√2', '1.5', '3/4'],
            'options_kn': ['0', '√2', '1.5', '3/4'],
            'correct_answer': '0',
            'explanation_en': '0 is a rational, whole, and natural number.',
            'explanation_hi': '0 एक परिमेय, पूर्ण और प्राकृत संख्या है।',
            'explanation_kn': '0 ಒಂದು ಭಿನ್ನರಾಶಿಯ, ಪೂರ್ಣ ಮತ್ತು ಸ್ವಾಭಾವಿಕ ಸಂಖ್ಯೆಯಾಗಿದೆ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        },
        {
            'question_en': 'Simplify: (x + 2)(x + 3)',
            'question_hi': 'सरल कीजिए: (x + 2)(x + 3)',
            'question_kn': 'ಸರಳಗೊಳಿಸಿ: (x + 2)(x + 3)',
            'options_en': ['x² + 5x + 6', 'x² + 6x + 5', 'x² + 2x + 3', 'x² + 3x + 2'],
            'options_hi': ['x² + 5x + 6', 'x² + 6x + 5', 'x² + 2x + 3', 'x² + 3x + 2'],
            'options_kn': ['x² + 5x + 6', 'x² + 6x + 5', 'x² + 2x + 3', 'x² + 3x + 2'],
            'correct_answer': 'x² + 5x + 6',
            'explanation_en': 'Use FOIL: x² + 3x + 2x + 6 = x² + 5x + 6.',
            'explanation_hi': 'FOIL का उपयोग करें: x² + 3x + 2x + 6 = x² + 5x + 6।',
            'explanation_kn': 'FOIL ಬಳಸಿ: x² + 3x + 2x + 6 = x² + 5x + 6.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'Triangle with angles 60°, 60°, 60° is called?',
            'question_hi': '60°, 60°, 60° कोणों वाला त्रिभुज क्या कहलाता है?',
            'question_kn': '60°, 60°, 60° ಕೋನಗಳ ತ್ರಿಭುಜವನ್ನು ಏನೆಂದು ಕರೆಯಲಾಗುತ್ತದೆ?',
            'options_en': ['Isosceles', 'Right', 'Equilateral', 'Scalene'],
            'options_hi': ['समद्विबाहु', 'समकोण', 'समबाहु', 'विषमबाहु'],
            'options_kn': ['ಐಸಾಸೆಲೀಸ್', 'ಲಂಬಕೋನ', 'ಸಮಬಾಹು', 'ಸ್ಕೇಲೀನ್'],
            'correct_answer': 'Equilateral',
            'explanation_en': 'All angles and sides are equal in an equilateral triangle.',
            'explanation_hi': 'समबाहु त्रिभुज में सभी कोण और भुजाएँ समान होती हैं।',
            'explanation_kn': 'ಸಮಬಾಹು ತ್ರಿಭುಜದಲ್ಲಿ ಎಲ್ಲಾ ಕೋನಗಳು ಮತ್ತು ಭುಜಗಳು ಸಮಾನವಾಗಿರುತ್ತವೆ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'Add: (2x² + 3x + 1) + (x² + 2x + 5)',
            'question_hi': 'जोड़ें: (2x² + 3x + 1) + (x² + 2x + 5)',
            'question_kn': 'ಕೂಡಿಸಿ: (2x² + 3x + 1) + (x² + 2x + 5)',
            'options_en': ['3x² + 5x + 6', '3x² + 6x + 6', 'x² + 5x + 6', '3x² + 5x + 5'],
            'options_hi': ['3x² + 5x + 6', '3x² + 6x + 6', 'x² + 5x + 6', '3x² + 5x + 5'],
            'options_kn': ['3x² + 5x + 6', '3x² + 6x + 6', 'x² + 5x + 6', '3x² + 5x + 5'],
            'correct_answer': '3x² + 5x + 6',
            'explanation_en': 'Add like terms: (2x² + x²), (3x + 2x), (1 + 5).',
            'explanation_hi': 'समान पदों को जोड़ें: (2x² + x²), (3x + 2x), (1 + 5)।',
            'explanation_kn': 'ಒಂದೇ ರೀತಿಯ ಪದಗಳನ್ನು ಕೂಡಿಸಿ: (2x² + x²), (3x + 2x), (1 + 5).',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'Which number is an irrational number?',
            'question_hi': 'कौन सी संख्या अपरिमेय है?',
            'question_kn': 'ಯಾವ ಸಂಖ್ಯೆಯು ಅಪರಿಮಿತವಾಗಿದೆ?',
            'options_en': ['4', '3/5', '√2', '0'],
            'options_hi': ['4', '3/5', '√2', '0'],
            'options_kn': ['4', '3/5', '√2', '0'],
            'correct_answer': '√2',
            'explanation_en': '√2 is irrational because it is non-terminating and non-repeating.',
            'explanation_hi': '√2 अपरिमेय है क्योंकि यह गैर-अंतिम और गैर-दोहराने वाला है।',
            'explanation_kn': '√2 ಅಪರಿಮಿತವಾಗಿದೆ ಏಕೆಂದರೆ ಇದು ಅಂತ್ಯವಾಗದ ಮತ್ತು ಪುನರಾವರ್ತನೆಯಾಗದ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        },
        {
            'question_en': 'What is the zero of the polynomial x - 3?',
            'question_hi': 'x - 3 बहुपद का शून्य क्या है?',
            'question_kn': 'x - 3 ಬಹುಪದದ ಶೂನ್ಯ ಎಷ್ಟು?',
            'options_en': ['0', '3', '-3', '1'],
            'options_hi': ['0', '3', '-3', '1'],
            'options_kn': ['0', '3', '-3', '1'],
            'correct_answer': '3',
            'explanation_en': 'x - 3 = 0 => x = 3.',
            'explanation_hi': 'x - 3 = 0 => x = 3।',
            'explanation_kn': 'x - 3 = 0 => x = 3.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'A triangle has angles 90°, 45°, and 45°. What type is it?',
            'question_hi': '90°, 45°, और 45° कोणों वाला त्रिभुज किस प्रकार का है?',
            'question_kn': '90°, 45°, ಮತ್ತು 45° ಕೋನಗಳ ತ್ರಿಭುಜ ಯಾವ ಪ್ರಕಾರದ್ದು?',
            'options_en': ['Scalene', 'Right-angled isosceles', 'Equilateral', 'Obtuse'],
            'options_hi': ['विषमबाहु', 'समकोण समद्विबाहु', 'समबाहु', 'अधिककोण'],
            'options_kn': ['ಸ್ಕೇಲೀನ್', 'ಲಂಬಕೋನ ಐಸಾಸೆಲೀಸ್', 'ಸಮಬಾಹು', 'ಒಬ್ಟೂಸ್'],
            'correct_answer': 'Right-angled isosceles',
            'explanation_en': '90° makes it right-angled; two equal 45° makes it isosceles.',
            'explanation_hi': '90° इसे समकोण बनाता है; दो समान 45° इसे समद्विबाहु बनाते हैं।',
            'explanation_kn': '90° ಇದನ್ನು ಲಂಬಕೋನವಾಗಿಸುತ್ತದೆ; ಎರಡು ಸಮಾನ 45° ಇದನ್ನು ಐಸಾಸೆಲೀಸ್ ಆಗಿಸುತ್ತದೆ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'Is 0 a rational number?',
            'question_hi': 'क्या 0 एक परिमेय संख्या है?',
            'question_kn': '0 ಒಂದು ಭಿನ್ನರಾಶಿಯ ಸಂಖ್ಯೆಯೇ?',
            'options_en': ['Yes', 'No', 'Sometimes', 'Only with integers'],
            'options_hi': ['हाँ', 'नहीं', 'कभी-कभी', 'केवल पूर्णांकों के साथ'],
            'options_kn': ['ಹೌದು', 'ಇಲ್ಲ', 'ಕೆಲವೊಮ್ಮೆ', 'ಕೇವಲ ಪೂರ್ಣಾಂಕಗಳೊಂದಿಗೆ'],
            'correct_answer': 'Yes',
            'explanation_en': '0 can be written as 0/1, so it is rational.',
            'explanation_hi': '0 को 0/1 के रूप में लिखा जा सकता है, इसलिए यह परिमेय है।',
            'explanation_kn': '0 ಅನ್ನು 0/1 ಎಂದು ಬರೆಯಬಹುದು, ಆದ್ದರಿಂದ ಇದು ಭಿನ್ನರಾಶಿಯಾಗಿದೆ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        },
        {
            'question_en': 'Subtract: (3x² + 2x + 1) - (x² + x + 1)',
            'question_hi': 'घटाएँ: (3x² + 2x + 1) - (x² + x + 1)',
            'question_kn': 'ಕಳೆಯಿರಿ: (3x² + 2x + 1) - (x² + x + 1)',
            'options_en': ['2x² + x + 0', 'x² + x + 2', '2x² + x', '2x² + x + 1'],
            'options_hi': ['2x² + x + 0', 'x² + x + 2', '2x² + x', '2x² + x + 1'],
            'options_kn': ['2x² + x + 0', 'x² + x + 2', '2x² + x', '2x² + x + 1'],
            'correct_answer': '2x² + x',
            'explanation_en': 'Subtract like terms: 3x² - x² = 2x², 2x - x = x, 1 - 1 = 0.',
            'explanation_hi': 'समान पदों को घटाएँ: 3x² - x² = 2x², 2x - x = x, 1 - 1 = 0।',
            'explanation_kn': 'ಒಂದೇ ರೀತಿಯ ಪದಗಳನ್ನು ಕಳೆಯಿರಿ: 3x² - x² = 2x², 2x - x = x, 1 - 1 = 0.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'What is the value of π (pi) up to two decimal places?',
            'question_hi': 'π (पाई) का मान दो दशमलव स्थानों तक क्या है?',
            'question_kn': 'π (ಪೈ) ರ ಮೌಲ್ಯವನ್ನು ಎರಡು ದಶಮಾಂಶ ಸ್ಥಾನಗಳವರೆಗೆ ಎಷ್ಟು?',
            'options_en': ['3.14', '3.12', '3.15', '3.10'],
            'options_hi': ['3.14', '3.12', '3.15', '3.10'],
            'options_kn': ['3.14', '3.12', '3.15', '3.10'],
            'correct_answer': '3.14',
            'explanation_en': 'Pi (π) is approximately 3.14.',
            'explanation_hi': 'पाई (π) लगभग 3.14 है।',
            'explanation_kn': 'ಪೈ (π) ಸರಿಸುಮಾರು 3.14 ಆಗಿದೆ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        },
        {
            'question_en': 'Two angles of a triangle are 80° and 50°. What is the third?',
            'question_hi': 'त्रिभुज के दो कोण 80° और 50° हैं। तीसरा क्या है?',
            'question_kn': 'ತ್ರಿಭುಜದ ಎರಡು ಕೋನಗಳು 80° ಮತ್ತು 50°. ಮೂರನೇ ಕೋನ ಎಷ್ಟು?',
            'options_en': ['40°', '30°', '50°', '60°'],
            'options_hi': ['40°', '30°', '50°', '60°'],
            'options_kn': ['40°', '30°', '50°', '60°'],
            'correct_answer': '50°',
            'explanation_en': '180° - (80° + 50°) = 50°.',
            'explanation_hi': '180° - (80° + 50°) = 50°।',
            'explanation_kn': '180° - (80° + 50°) = 50°.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'What is the multiplicative identity in real numbers?',
            'question_hi': 'वास्तविक संख्याओं में गुणनात्मक सर्वसमिका क्या है?',
            'question_kn': 'ವಾಸ್ತವಿಕ ಸಂಖ್ಯೆಗಳಲ್ಲಿ ಗುಣಾಕಾರದ ಸರ್ವಸಮತೆ ಎಂದರೇನು?',
            'options_en': ['0', '1', '-1', '10'],
            'options_hi': ['0', '1', '-1', '10'],
            'options_kn': ['0', '1', '-1', '10'],
            'correct_answer': '1',
            'explanation_en': 'Any number × 1 = the number itself.',
            'explanation_hi': 'कोई भी संख्या × 1 = वह संख्या स्वयं।',
            'explanation_kn': 'ಯಾವುದೇ ಸಂಖ್ಯೆ × 1 = ಆ ಸಂಖ್ಯೆಯೇ.',
            'type': 'Math_9th',
            'difficulty': 'easy',
            'chapter': 'Number Systems'
        }
    ],
    '10th': [
        {
            'question_en': 'What is the value of sin 30°?',
            'question_hi': 'sin 30° का मान क्या है?',
            'question_kn': 'sin 30° ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['1/2', '√3/2', '1', '0'],
            'options_hi': ['1/2', '√3/2', '1', '0'],
            'options_kn': ['1/2', '√3/2', '1', '0'],
            'correct_answer': '1/2',
            'explanation_en': 'From trigonometry, sin 30° = 1/2.',
            'explanation_hi': 'त्रिकोणमिति से, sin 30° = 1/2।',
            'explanation_kn': 'ತ್ರಿಕೋನಮಿತಿಯಿಂದ, sin 30° = 1/2.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Trigonometry'
        },
        {
            'question_en': 'Solve for x: 2x + 3 = 7',
            'question_hi': 'x के लिए हल करें: 2x + 3 = 7',
            'question_kn': 'x ಗಾಗಿ ಪರಿಹರಿಸಿ: 2x + 3 = 7',
            'options_en': ['1', '2', '3', '4'],
            'options_hi': ['1', '2', '3', '4'],
            'options_kn': ['1', '2', '3', '4'],
            'correct_answer': '2',
            'explanation_en': '2x + 3 = 7 => 2x = 4 => x = 2.',
            'explanation_hi': '2x + 3 = 7 => 2x = 4 => x = 2।',
            'explanation_kn': '2x + 3 = 7 => 2x = 4 => x = 2.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Linear Equations'
        },
        {
            'question_en': 'What is the sum of first n natural numbers?',
            'question_hi': 'पहले n प्राकृत संख्याओं का योग क्या है?',
            'question_kn': 'ಮೊದಲ n ಸ್ವಾಭಾವಿಕ ಸಂಖ್ಯೆಗಳ ಮೊತ್ತ ಎಷ್ಟು?',
            'options_en': ['n(n+1)/2', 'n²', 'n(n-1)/2', 'n²/2'],
            'options_hi': ['n(n+1)/2', 'n²', 'n(n-1)/2', 'n²/2'],
            'options_kn': ['n(n+1)/2', 'n²', 'n(n-1)/2', 'n²/2'],
            'correct_answer': 'n(n+1)/2',
            'explanation_en': 'Sum of first n natural numbers = n(n+1)/2.',
            'explanation_hi': 'पहले n प्राकृत संख्याओं का योग = n(n+1)/2।',
            'explanation_kn': 'ಮೊದಲ n ಸ್ವಾಭಾವಿಕ ಸಂಖ್ಯೆಗಳ ಮೊತ್ತ = n(n+1)/2.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Real Numbers'
        },
        {
            'question_en': 'What is the area of a triangle with base 6 cm and height 4 cm?',
            'question_hi': '6 सेमी आधार और 4 सेमी ऊँचाई वाले त्रिभुज का क्षेत्रफल क्या है?',
            'question_kn': '6 ಸೆಂ.ಮೀ ಆಧಾರ ಮತ್ತು 4 ಸೆಂ.ಮೀ ಎತ್ತರದ ತ್ರಿಭುಜದ ವಿಸ್ತೀರ್ಣ ಎಷ್ಟು?',
            'options_en': ['12 cm²', '24 cm²', '10 cm²', '18 cm²'],
            'options_hi': ['12 सेमी²', '24 सेमी²', '10 सेमी²', '18 सेमी²'],
            'options_kn': ['12 ಸೆಂ.ಮೀ²', '24 ಸೆಂ.ಮೀ²', '10 ಸೆಂ.ಮೀ²', '18 ಸೆಂ.ಮೀ²'],
            'correct_answer': '12 cm²',
            'explanation_en': 'Area = ½ × base × height = ½ × 6 × 4 = 12 cm².',
            'explanation_hi': 'क्षेत्रफल = ½ × आधार × ऊँचाई = ½ × 6 × 4 = 12 सेमी²।',
            'explanation_kn': 'ವಿಸ್ತೀರ್ಣ = ½ × ಆಧಾರ × ಎತ್ತರ = ½ × 6 × 4 = 12 ಸೆಂ.ಮೀ².',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'What is the value of cos 0°?',
            'question_hi': 'cos 0° का मान क्या है?',
            'question_kn': 'cos 0° ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['0', '1', '√3/2', '1/2'],
            'options_hi': ['0', '1', '√3/2', '1/2'],
            'options_kn': ['0', '1', '√3/2', '1/2'],
            'correct_answer': '1',
            'explanation_en': 'cos 0° = 1 in trigonometry.',
            'explanation_hi': 'त्रिकोणमिति में cos 0° = 1।',
            'explanation_kn': 'ತ್ರಿಕೋನಮಿತಿಯಲ್ಲಿ cos 0° = 1.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Trigonometry'
        },
        {
            'question_en': 'Find the zero of the polynomial x - 5.',
            'question_hi': 'x - 5 बहुपद का शून्य ज्ञात कीजिए।',
            'question_kn': 'x - 5 ಬಹುಪದದ ಶೂನ್ಯವನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ.',
            'options_en': ['5', '0', '-5', '1'],
            'options_hi': ['5', '0', '-5', '1'],
            'options_kn': ['5', '0', '-5', '1'],
            'correct_answer': '5',
            'explanation_en': 'x - 5 = 0 ⇒ x = 5.',
            'explanation_hi': 'x - 5 = 0 ⇒ x = 5।',
            'explanation_kn': 'x - 5 = 0 ⇒ x = 5.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'Is √3 rational or irrational?',
            'question_hi': 'क्या √3 परिमेय है या अपरिमेय?',
            'question_kn': '√3 ಭಿನ್ನರಾಶಿಯಾ ಅಥವಾ ಅಪರಿಮಿತವೇ?',
            'options_en': ['Rational', 'Irrational', 'Whole number', 'Integer'],
            'options_hi': ['परिमेय', 'अपरिमेय', 'पूर्ण संख्या', 'पूर्णांक'],
            'options_kn': ['ಭಿನ್ನರಾಶಿ', 'ಅಪರಿಮಿತ', 'ಪೂರ್ಣ ಸಂಖ್ಯೆ', 'ಪೂರ್ಣಾಂಕ'],
            'correct_answer': 'Irrational',
            'explanation_en': '√3 is a non-terminating, non-repeating decimal ⇒ Irrational.',
            'explanation_hi': '√3 गैर-अंतिम, गैर-दोहराने वाला दशमलव है ⇒ अपरिमेय।',
            'explanation_kn': '√3 ಒಂದು ಅಂತ್ಯವಾಗದ, ಪುನರಾವರ್ತನೆಯಾಗದ ದಶಮಾಂಶ ⇒ ಅಪರಿಮಿತ.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Real Numbers'
        },
        {
            'question_en': 'Solve: x² - 9 = 0',
            'question_hi': 'हल करें: x² - 9 = 0',
            'question_kn': 'ಪರಿಹರಿಸಿ: x² - 9 = 0',
            'options_en': ['x = ±3', 'x = 9', 'x = 0', 'x = 3'],
            'options_hi': ['x = ±3', 'x = 9', 'x = 0', 'x = 3'],
            'options_kn': ['x = ±3', 'x = 9', 'x = 0', 'x = 3'],
            'correct_answer': 'x = ±3',
            'explanation_en': 'x² = 9 ⇒ x = ±√9 = ±3.',
            'explanation_hi': 'x² = 9 ⇒ x = ±√9 = ±3।',
            'explanation_kn': 'x² = 9 ⇒ x = ±√9 = ±3.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'Which identity is used in (a + b)²?',
            'question_hi': '(a + b)² में कौन सी सर्वसमिका उपयोग की जाती है?',
            'question_kn': '(a + b)² ರಲ್ಲಿ ಯಾವ ಸರ್ವಸಮತೆಯನ್ನು ಬಳಸಲಾಗುತ್ತದೆ?',
            'options_en': ['a² - 2ab + b²', 'a² + 2ab + b²', '(a - b)(a + b)', 'a² + b²'],
            'options_hi': ['a² - 2ab + b²', 'a² + 2ab + b²', '(a - b)(a + b)', 'a² + b²'],
            'options_kn': ['a² - 2ab + b²', 'a² + 2ab + b²', '(a - b)(a + b)', 'a² + b²'],
            'correct_answer': 'a² + 2ab + b²',
            'explanation_en': '(a + b)² = a² + 2ab + b².',
            'explanation_hi': '(a + b)² = a² + 2ab + b²।',
            'explanation_kn': '(a + b)² = a² + 2ab + b².',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'What is the value of tan 45°?',
            'question_hi': 'tan 45° का मान क्या है?',
            'question_kn': 'tan 45° ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['1', '0', '√3', '∞'],
            'options_hi': ['1', '0', '√3', '∞'],
            'options_kn': ['1', '0', '√3', '∞'],
            'correct_answer': '1',
            'explanation_en': 'tan 45° = 1 in trigonometry.',
            'explanation_hi': 'त्रिकोणमिति में tan 45° = 1।',
            'explanation_kn': 'ತ್ರಿಕೋನಮಿತಿಯಲ್ಲಿ tan 45° = 1.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Trigonometry'
        },
        {
            'question_en': 'If x = 3, what is the value of 2x²?',
            'question_hi': 'यदि x = 3, तो 2x² का मान क्या है?',
            'question_kn': 'x = 3 ಆಗಿದ್ದರೆ, 2x² ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
            'options_en': ['6', '9', '18', '12'],
            'options_hi': ['6', '9', '18', '12'],
            'options_kn': ['6', '9', '18', '12'],
            'correct_answer': '18',
            'explanation_en': '2 × 3² = 2 × 9 = 18.',
            'explanation_hi': '2 × 3² = 2 × 9 = 18।',
            'explanation_kn': '2 × 3² = 2 × 9 = 18.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Polynomials'
        },
        {
            'question_en': 'Which of the following is not a real number?',
            'question_hi': 'निम्नलिखित में से कौन सा वास्तविक संख्या नहीं है?',
            'question_kn': 'ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು ವಾಸ್ತವಿಕ ಸಂಖ್ಯೆಯಲ್ಲ?',
            'options_en': ['0', '√2', '3/5', '√(-1)'],
            'options_hi': ['0', '√2', '3/5', '√(-1)'],
            'options_kn': ['0', '√2', '3/5', '√(-1)'],
            'correct_answer': '√(-1)',
            'explanation_en': 'Square root of a negative number is imaginary.',
            'explanation_hi': 'नकारात्मक संख्या का वर्गमूल काल्पनिक होता है।',
            'explanation_kn': 'ಋಣಾತ್ಮಕ ಸಂಖ್ಯೆಯ ವರ್ಗಮೂಲ ಕಾಲ್ಪನಿಕವಾಗಿದೆ.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Real Numbers'
        },
        {
            'question_en': 'Which triangle theorem relates sides and sine of angles?',
            'question_hi': 'कौन सा त्रिभुज प्रमेय भुजाओं और कोणों की ज्या से संबंधित है?',
            'question_kn': 'ಯಾವ ತ್ರಿಭುಜ ಪ್ರಮೇಯವು ಭುಜಗಳು ಮತ್ತು ಕೋನಗಳ ಸೈನ್‌ಗೆ ಸಂಬಂಧಿಸಿದೆ?',
            'options_en': ['Sine Rule', 'Pythagoras', 'Cosine Rule', 'Area Theorem'],
            'options_hi': ['ज्या नियम', 'पाइथागोरस', 'कोज्या नियम', 'क्षेत्रफल प्रमेय'],
            'options_kn': ['ಸೈನ್ ನಿಯಮ', 'ಪೈಥಾಗೋರಸ್', 'ಕೊಸೈನ್ ನಿಯಮ', 'ವಿಸ್ತೀರ್ಣ ಪ್ರಮೇಯ'],
            'correct_answer': 'Sine Rule',
            'explanation_en': 'The sine rule relates the ratio of side length to the sine of the opposite angle.',
            'explanation_hi': 'ज्या नियम भुजा की लंबाई और सामने के कोण की ज्या के अनुपात को जोड़ता है।',
            'explanation_kn': 'ಸೈನ್ ನಿಯಮವು ಭುಜದ ಉದ್ದದ ಅನುಪಾತವನ್ನು ಎದುರಿನ ಕೋನದ ಸೈನ್‌ಗೆ ಸಂಬಂಧಿಸುತ್ತದೆ.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'In right triangle ABC, if ∠C = 90°, then which side is the hypotenuse?',
            'question_hi': 'समकोण त्रिभुज ABC में, यदि ∠C = 90°, तो कौन सी भुजा कर्ण है?',
            'question_kn': 'ಲಂಬಕೋನ ತ್ರಿಭುಜ ABC ಯಲ್ಲಿ, ∠C = 90° ಆಗಿದ್ದರೆ, ಯಾವ ಭುಜವು ಕರ್ಣವಾಗಿದೆ?',
            'options_en': ['AB', 'BC', 'AC', 'None'],
            'options_hi': ['AB', 'BC', 'AC', 'कोई नहीं'],
            'options_kn': ['AB', 'BC', 'AC', 'ಯಾವುದೂ ಇಲ್ಲ'],
            'correct_answer': 'AB',
            'explanation_en': 'Side opposite the right angle (∠C) is hypotenuse ⇒ AB.',
            'explanation_hi': 'समकोण (∠C) के सामने की भुजा कर्ण है ⇒ AB।',
            'explanation_kn': 'ಲಂಬಕೋನ (∠C) ಎದುರಿನ ಭುಜವು ಕರ್ಣವಾಗಿದೆ ⇒ AB.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Triangles'
        },
        {
            'question_en': 'What is the standard form of a linear equation in two variables?',
            'question_hi': 'दो चरों में रैखिक समीकरण का मानक रूप क्या है?',
            'question_kn': 'ಎರಡು ಚರಗಳಲ್ಲಿ ರೇಖೀಯ ಸಮೀಕರಣದ ಗುಣಮಟ್ಟದ ರೂಪ ಯಾವುದು?',
            'options_en': ['ax + by = c', 'ax² + bx + c = 0', 'x = y', 'x² = y'],
            'options_hi': ['ax + by = c', 'ax² + bx + c = 0', 'x = y', 'x² = y'],
            'options_kn': ['ax + by = c', 'ax² + bx + c = 0', 'x = y', 'x² = y'],
            'correct_answer': 'ax + by = c',
            'explanation_en': 'This is the standard form where a, b, c are real constants.',
            'explanation_hi': 'यह मानक रूप है जहाँ a, b, c वास्तविक स्थिरांक हैं।',
            'explanation_kn': 'ಇದು ಗುಣಮಟ್ಟದ ರೂಪವಾಗಿದೆ, ಇಲ್ಲಿ a, b, c ವಾಸ್ತವಿಕ ಸ್ಥಿರಾಂಕಗಳಾಗಿವೆ.',
            'type': 'Math_10th',
            'difficulty': 'easy',
            'chapter': 'Linear Equations'
        },
        {
'question_en': 'Find the LCM of 4 and 6.',
'question_hi': '4 और 6 का LCM ज्ञात कीजिए।',
'question_kn': '4 ಮತ್ತು 6 ರ LCM ಕಂಡುಹಿಡಿಯಿರಿ.',
'options_en': ['2', '12', '24', '8'],
'options_hi': ['2', '12', '24', '8'],
'options_kn': ['2', '12', '24', '8'],
'correct_answer': '12',
'explanation_en': 'LCM of 4 and 6 = 12.',
'explanation_hi': '4 और 6 का LCM = 12।',
'explanation_kn': '4 ಮತ್ತು 6 ರ LCM = 12.',
'type': 'Math_10th',
'difficulty': 'easy',
'chapter': 'Real Numbers'
},
{
'question_en': 'What is the discriminant in quadratic equations?',
'question_hi': 'द्विघात समीकरणों में विविक्तकर क्या है?',
'question_kn': 'ದ್ವಿಘಾತ ಸಮೀಕರಣಗಳಲ್ಲಿ ವಿವಿಕ್ತಕ ಎಂದರೇನು?',
'options_en': ['b² - 4ac', 'a² + b²', 'b² + 4ac', 'a + b + c'],
'options_hi': ['b² - 4ac', 'a² + b²', 'b² + 4ac', 'a + b + c'],
'options_kn': ['b² - 4ac', 'a² + b²', 'b² + 4ac', 'a + b + c'],
'correct_answer': 'b² - 4ac',
'explanation_en': 'Discriminant D = b² - 4ac is used to determine nature of roots.',
'explanation_hi': 'विविक्तकर D = b² - 4ac का उपयोग जड़ों की प्रकृति निर्धारित करने के लिए किया जाता है।',
'explanation_kn': 'ವಿವಿಕ್ತಕ D = b² - 4ac ಅನ್ನು ಜಡಗಳ ಸ್ವರೂಪವನ್ನು ನಿರ್ಧರಿಸಲು ಬಳಸಲಾಗುತ್ತದೆ.',
'type': 'Math_10th',
'difficulty': 'easy',
'chapter': 'Polynomials'
},
{
'question_en': 'What is sin 0°?',
'question_hi': 'sin 0° का मान क्या है?',
'question_kn': 'sin 0° ರ ಮೌಲ್ಯ ಎಷ್ಟು?',
'options_en': ['0', '1', 'Undefined', '1/2'],
'options_hi': ['0', '1', 'अपरिभाषित', '1/2'],
'options_kn': ['0', '1', 'ವ್ಯಾಖ್ಯಾನಿಸದ', '1/2'],
'correct_answer': '0',
'explanation_en': 'sin 0° = 0.',
'explanation_hi': 'sin 0° = 0।',
'explanation_kn': 'sin 0° = 0.',
'type': 'Math_10th',
'difficulty': 'easy',
'chapter': 'Trigonometry'
},
{
'question_en': 'Is x = 5, y = 2 a solution of 2x + y = 12?',
'question_hi': 'क्या x = 5, y = 2 समीकरण 2x + y = 12 का हल है?',
'question_kn': 'x = 5, y = 2 ಎಂಬುದು 2x + y = 12 ಸಮೀಕರಣದ ಪರಿಹಾರವೇ?',
'options_en': ['Yes', 'No', 'Only if y=3', 'Only if x=3'],
'options_hi': ['हाँ', 'नहीं', 'केवल यदि y=3', 'केवल यदि x=3'],
'options_kn': ['ಹೌದು', 'ಇಲ್ಲ', 'ಕೇವಲ y=3 ಆಗಿದ್ದರೆ', 'ಕೇವಲ x=3 ಆಗಿದ್ದರೆ'],
'correct_answer': 'Yes',
'explanation_en': '2×5 + 2 = 10 + 2 = 12. It satisfies the equation.',
'explanation_hi': '2×5 + 2 = 10 + 2 = 12। यह समीकरण को संतुष्ट करता है।',
'explanation_kn': '2×5 + 2 = 10 + 2 = 12. ಇದು ಸಮೀಕರಣವನ್ನು ತೃಪ್ತಿಗೊಳಿಸುತ್ತದೆ.',
'type': 'Math_10th',
'difficulty': 'easy',
'chapter': 'Linear Equations'
},
{
'question_en': 'Which theorem states that in a right triangle, square of hypotenuse = sum of squares of other sides?',
'question_hi': 'कौन सा प्रमेय कहता है कि समकोण त्रिभुज में, कर्ण का वर्ग = अन्य भुजाओं के वर्गों का योग?',
'question_kn': 'ಯಾವ ಪ್ರಮೇಯವು ಲಂಬಕೋನ ತ್ರಿಭುಜದಲ್ಲಿ, ಕರ್ಣದ ವರ್ಗ = ಇತರ ಭುಜಗಳ ವರ್ಗಗಳ ಮೊತ್ತ ಎಂದು ಹೇಳುತ್ತದೆ?',
'options_en': ['Pythagoras', 'Euclid’s', 'Basic Proportionality', 'Sine rule'],
'options_hi': ['पाइथागोरस', 'यूक्लिड', 'मूल समानुपात', 'ज्या नियम'],
'options_kn': ['ಪೈಥಾಗೋರಸ್', 'ಯೂಕ್ಲಿಡ್‌ನ', 'ಮೂಲಭೂತ ಸಮಾನತೆ', 'ಸೈನ್ ನಿಯಮ'],
'correct_answer': 'Pythagoras',
'explanation_en': 'a² + b² = c² in a right-angled triangle is Pythagoras Theorem.',
'explanation_hi': 'समकोण त्रिभुज में a² + b² = c² पाइथागोरस प्रमेय है।',
'explanation_kn': 'ಲಂಬಕೋನ ತ್ರಿಭುಜದಲ್ಲಿ a² + b² = c² ಎಂಬುದು ಪೈಥಾಗೋರಸ್ ಪ್ರಮೇಯವಾಗಿದೆ.',
'type': 'Math_10th',
'difficulty': 'easy',
'chapter': 'Triangles'
}
]
}

logging.getLogger("pymongo").setLevel(logging.WARNING)

app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient('mongodb+srv://apt:apt@apt.ydfi6pf.mongodb.net/?retryWrites=true&w=majority&appName=apt')
db = client['school']
users = db['users']
rooms = db['rooms']

APTITUDE_API_BASE_URL = 'https://aptitude-api.vercel.app'

def generate_questions(num_questions, difficulty, question_types, selection_mode):
    topic_map = {
        'mixture_alligation': 'MixtureAndAlligation',
        'profit_loss': 'ProfitAndLoss',
        'pipes_cisterns': 'PipesAndCistern',
        'age': 'Age',
        'permutation_combination': 'PermutationAndCombination',
        'speed_time_distance': 'SpeedTimeDistance',
        'simple_interest': 'SimpleInterest',
        'calendars': 'Calendar'
    }
    selected_topics = [topic_map.get(qt.lower(), 'Age') for qt in question_types] if question_types else ['Age']
    all_questions = []
    max_attempts = num_questions * 3
    attempts = 0

    while len(all_questions) < num_questions and attempts < max_attempts:
        topic = random.choice(selected_topics)
        params = {'amount': 1}
        try:
            response = requests.get(f"{APTITUDE_API_BASE_URL}/{topic}", params=params)
            response.raise_for_status()
            response_data = response.json()
            question_items = response_data if isinstance(response_data, list) else [response_data]
            for item in question_items:
                if 'question' in item and item['question'] not in [q['question'] for q in all_questions]:
                    all_questions.append({
                        'question': item.get('question', 'No question available'),
                        'options': item.get('options', ['A', 'B', 'C', 'D']),
                        'correct_answer': item.get('answer', 'N/A'),
                        'explanation': item.get('explanation', 'No explanation available'),
                        'type': topic,
                        'difficulty': difficulty if difficulty else 'Any'
                    })
                    break
        except requests.exceptions.RequestException:
            pass
        attempts += 1
    random.shuffle(all_questions)
    return all_questions[:num_questions], None

def generate_room_code():
    return ''.join(random.choices(string.digits, k=4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_language/<lang>')
def set_language(lang):
    session['language'] = lang
    return jsonify({'status': 'ok'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        role = request.form['role']
        user = users.find_one({'name': name, 'role': role})
        if user and bcrypt.checkpw(password, user['password']):
            session['user_id'] = str(user['_id'])
            session['role'] = role
            session['name'] = name
            logger.debug(f"User {name} ({role}) logged in with session: {session}")
            if role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid name, password, or role')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        role = request.form['role']
        if users.find_one({'name': name, 'role': role}):
            return render_template('register.html', error='User with this name and role already exists')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        users.insert_one({'name': name, 'password': hashed, 'role': role})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    language = request.cookies.get('language', 'en')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = users.find_one({'_id': ObjectId(session['user_id'])})
    language = session.get('language', 'en')
    return render_template('dashboard.html', user=user, language=language)


@app.route('/teacher_dashboard')
def teacher_dashboard():
    language = request.cookies.get('language', 'en')
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to teacher_dashboard: {session}")
        return redirect(url_for('login'))
    user = users.find_one({'_id': ObjectId(session['user_id'])})
    active_rooms = list(rooms.find({'teacher_id': session['user_id'], 'status': {'$in': ['active', 'started', 'stopped']}}))
    for room in active_rooms:
        room['_id'] = str(room['_id'])
        room['num_students'] = len(room.get('students', []))
    language = session.get('language', 'en')
    return render_template('dashboard1.html', user=user, active_rooms=active_rooms, language=session.get('language', 'en'))

@app.route('/analytics')
def analytics():
    language = request.cookies.get('language', 'en')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_name = session['name']
    user_collection = db[user_name]
    quizzes = list(user_collection.find({'results': {'$exists': True}}))
    for quiz in quizzes:
        correct = quiz.get('score', 0)
        total = quiz.get('num_questions', 0)
        incorrect = total - correct
        quiz['_id'] = str(quiz['_id'])
        quiz['correct'] = correct
        quiz['incorrect'] = incorrect
        quiz['date'] = quiz.get('completed_at').strftime('%Y-%m-%d') if quiz.get('completed_at') else 'N/A'
    language = session.get('language', 'en')
    return render_template('analytics.html', quizzes=quizzes, language=language)

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    language = request.cookies.get('language', 'en')
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        num_questions = int(request.form['num_questions'])
        difficulty = request.form['difficulty']
        question_types = request.form.getlist('question_types')
        selection_mode = request.form['selection_mode']

        math_types = [qt for qt in question_types if qt.startswith('Math_')]
        non_math_types = [qt for qt in question_types if not qt.startswith('Math_')]

        questions = []
        error = None

        # --- NCERT Maths Logic ---
        for mtype in math_types:
            try:
                level = mtype.split('_')[1]  # e.g., '8th'
                if level in NCERT_QUESTION_BANK:
                    filtered = [q for q in NCERT_QUESTION_BANK[level] if q['difficulty'] == difficulty and q['type'] == mtype]
                    random.shuffle(filtered)
                    questions += filtered[:num_questions]
            except Exception as e:
                error = f"Error processing math category {mtype}: {e}"

        # --- API for non-Maths ---
        if non_math_types:
            api_questions, api_error = generate_questions(num_questions, difficulty, non_math_types, selection_mode)
            if api_error:
                error = api_error
            questions += api_questions

        if not questions:
            return render_template('create_quiz.html', error=error or "No questions found.", language=language)

        user_name = session['name']
        user_collection = db[user_name]

        quiz_data = {
            'quiz_name': quiz_name,
            'num_questions': len(questions),
            'difficulty': difficulty,
            'question_types': question_types,
            'selection_mode': selection_mode,
            'questions': questions,
            'created_at': datetime.datetime.now()
        }

        quiz_id = user_collection.insert_one(quiz_data).inserted_id
        return redirect(url_for('take_quiz', quiz_id=str(quiz_id)))

    return render_template('create_quiz.html', language=language)



@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        num_questions = int(request.form['num_questions'])
        difficulty = request.form['difficulty']
        question_types = request.form.getlist('question_types')
        selection_mode = request.form['selection_mode']
        language = request.cookies.get('language', 'en')  # Get user-selected language

        math_types = [qt for qt in question_types if qt.startswith('Math_')]
        non_math_types = [qt for qt in question_types if not qt.startswith('Math_')]

        questions = []
        error = None

        # NCERT-based maths
        for mtype in math_types:
            grade = mtype.replace('Math_', '')
            if grade in NCERT_QUESTION_BANK:
                filtered = [q for q in NCERT_QUESTION_BANK[grade] if q['difficulty'] == difficulty]
                random.shuffle(filtered)
                selected = filtered[:num_questions]

                for q in selected:
                    if language == 'hi':
                        q['question'] = q.get('question_hi', q['question'])
                        q['options'] = q.get('options_hi', q['options'])
                        q['explanation'] = q.get('explanation_hi', q.get('explanation'))
                    elif language == 'kn':
                        q['question'] = q.get('question_kn', q['question'])
                        q['options'] = q.get('options_kn', q['options'])
                        q['explanation'] = q.get('explanation_kn', q.get('explanation'))
                    # Add English fallback (already default)
                    questions.append(q)

        # Handle non-math questions from API
        if non_math_types:
            api_questions, api_error = generate_questions(num_questions, difficulty, non_math_types, selection_mode)
            if api_error:
                error = api_error
            questions += api_questions

        if not questions:
            return render_template('create_room.html', error=error or "No questions found.", language=language)

        # Create room
        room_code = generate_room_code()
        while rooms.find_one({'room_code': room_code}):
            room_code = generate_room_code()

        room_data = {
            'quiz_name': quiz_name,
            'num_questions': len(questions),
            'difficulty': difficulty,
            'question_types': question_types,
            'selection_mode': selection_mode,
            'questions': questions,
            'room_code': room_code,
            'teacher_id': session['user_id'],
            'students': [],
            'student_results': [],
            'status': 'active',
            'created_at': datetime.datetime.now()
        }

        rooms.insert_one(room_data)
        return redirect(url_for('room', room_id=str(rooms.find_one({'room_code': room_code})['_id'])))

    return render_template("create_room.html", language=session.get("language", "en"))




@app.route('/room/<room_id>')
def room(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to room {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    room['_id'] = str(room['_id'])
    room['num_students'] = len(room.get('students', []))
    language = session.get('language', 'en')
    return render_template("room.html", room=room, language=session.get("language", "en"))


@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    language = request.cookies.get('language', 'en')
    
    if 'user_id' not in session or session['role'] != 'student':
        logger.debug(f"Unauthorized access to join_room: {session}")
        return redirect(url_for('login'))
    if request.method == 'POST':
        room_code = request.form['room_code']
        room = rooms.find_one({'room_code': room_code, 'status': 'active'})
        if not room:
            return render_template('join_room.html', error='Invalid or inactive room code')
        user_name = session['name']
        if user_name not in room.get('students', []):
            rooms.update_one(
                {'_id': ObjectId(room['_id'])},
                {'$addToSet': {'students': user_name}}
            )
        return redirect(url_for('wait_room', room_id=str(room['_id'])))
    language = session.get('language', 'en')
    return render_template('join_room.html', error=None, language=language)



@app.route('/wait_room/<room_id>')
def wait_room(room_id):
    language = request.cookies.get('language', 'en')

    if 'user_id' not in session or session['role'] != 'student':
        logger.debug(f"Unauthorized access to wait_room {room_id}: {session}")
        return redirect(url_for('login'))

    room = rooms.find_one({'_id': ObjectId(room_id), 'status': {'$in': ['active', 'started', 'stopped']}})
    if not room or session['name'] not in room.get('students', []):
        return redirect(url_for('dashboard'))

    # Auto-redirect if already started
    if room['status'] == 'started':
        return redirect(url_for('take_room_quiz', room_id=room_id))

    # Set error message if stopped
    error = 'The quiz has been stopped by the teacher.' if room['status'] == 'stopped' else None

    # Get user's selected language
    language = session.get('language', 'en')

    return render_template('wait_room.html', room_id=room_id, error=error, language=language)


@app.route('/start_quiz/<room_id>')
def start_quiz(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to start_quiz {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    rooms.update_one(
        {'_id': ObjectId(room_id)},
        {'$set': {'status': 'started', 'start_time': datetime.datetime.now()}}
    )
    return redirect(url_for('room', room_id=room_id))

@app.route('/stop_quiz/<room_id>')
def stop_quiz(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to stop_quiz {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    rooms.update_one(
        {'_id': ObjectId(room_id)},
        {'$set': {'status': 'stopped', 'stop_time': datetime.datetime.now()}}
    )
    return redirect(url_for('room', room_id=room_id))


@app.route('/take_room_quiz/<room_id>', methods=['GET', 'POST'])
def take_room_quiz(room_id):
    language = session.get('language', 'en')  # ✅ Correct

    if 'user_id' not in session or session['role'] != 'student':
        logger.debug(f"Unauthorized access to take_room_quiz {room_id}: {session}")
        return redirect(url_for('login'))

    room = rooms.find_one({'_id': ObjectId(room_id)})
    if not room or session['name'] not in room.get('students', []):
        return redirect(url_for('dashboard'))

    if room['status'] != 'started':
        error = 'The quiz is not active or has been stopped by the teacher.'
        return render_template('wait_room.html', room_id=room_id, error=error, language=language)  # ✅ pass language

    if 'current_question' not in session or 'room_id' not in session or session['room_id'] != room_id:
        session['current_question'] = 0
        session['room_id'] = room_id
        session['answers'] = {}
        questions = room['questions']
        random.shuffle(questions)
        session['questions'] = questions

    current_question = session['current_question']
    questions = session['questions']

    if request.method == 'POST':
        user_answer = request.form.get(f'question_{current_question}')
        if user_answer:
            session['answers'][str(current_question)] = user_answer

        if 'next' in request.form and current_question < len(questions) - 1:
            session['current_question'] = current_question + 1
            return redirect(url_for('take_room_quiz', room_id=room_id))

        elif 'submit_quiz' in request.form or current_question >= len(questions) - 1:
            room = rooms.find_one({'_id': ObjectId(room_id)})
            if room['status'] != 'started':
                error = 'The quiz has been stopped by the teacher.'
                return render_template('wait_room.html', room_id=room_id, error=error, language=language)

            answers = session.get('answers', {})
            score = 0
            results = []

            for i, question in enumerate(questions):
                user_answer = answers.get(str(i))
                correct = user_answer == question['correct_answer']
                if correct:
                    score += 1
                # Check if it's a translatable (NCERT) question
                q_text = question.get(f'question_{language}', question.get('question'))
                explanation_text = question.get(f'explanation_{language}', question.get('explanation'))
                options_text = question.get(f'options_{language}', question.get('options'))

                translated_correct = question.get(f'options_{language}', question.get('options', []))
                correct_answer_text = question['correct_answer']
                user_answer_text = user_answer

                # Translate correct_answer if it's an option
                if isinstance(translated_correct, list):
                    if correct_answer_text in question.get('options', []):
                        index = question['options'].index(correct_answer_text)
                        correct_answer_text = translated_correct[index] if index < len(translated_correct) else correct_answer_text
                    if user_answer in question.get('options', []):
                        index = question['options'].index(user_answer)
                        user_answer_text = translated_correct[index] if index < len(translated_correct) else user_answer

                results.append({
                    'question': q_text,
                    'user_answer': user_answer_text,
                    'correct_answer': correct_answer_text,
                    'correct': correct,
                    'explanation': explanation_text
                })





            user_name = session['name']
            user_collection = db[user_name]
            quiz_data = {
                'quiz_name': room['quiz_name'],
                'num_questions': room['num_questions'],
                'total_time': room.get('total_time', 0),
                'per_question_time': room.get('per_question_time', 0),
                'difficulty': room['difficulty'],
                'question_types': room['question_types'],
                'selection_mode': room['selection_mode'],
                'questions': [
    {
        **q,
        'question': q.get(f'question_{language}', q.get('question')),
        'options': q.get(f'options_{language}', q.get('options')),
        'explanation': q.get(f'explanation_{language}', q.get('explanation')),
    } for q in questions
],

                'results': results,
                'score': score,
                'room_id': room_id,
                'completed_at': datetime.datetime.now()
            }

            quiz_id = user_collection.insert_one(quiz_data).inserted_id
            rooms.update_one(
                {'_id': ObjectId(room_id)},
                {'$push': {'student_results': {
                    'name': user_name,
                    'score': score,
                    'results': results,
                    'quiz_id': str(quiz_id)
                }}}
            )

            session.pop('current_question', None)
            session.pop('answers', None)
            session.pop('room_id', None)
            session.pop('questions', None)
            

            translated_quiz = dict(room)
            translated_quiz['questions'] = [
                {
                    **q,
                    'question': q.get(f'question_{language}', q.get('question')),
                    'options': q.get(f'options_{language}', q.get('options')),
                    'explanation': q.get(f'explanation_{language}', q.get('explanation')),
                } for q in questions
            ]

            return render_template(
                'take_quiz.html',
                quiz=translated_quiz,
                results=results,
                score=score,
                show_results=True,
                room_id=room_id,
                quiz_id=str(quiz_id),
                language=language
            )

        
    language = session.get('language', 'en')


    return render_template(
        'take_quiz.html',
        quiz=room,
        current_question=current_question,
        room_id=room_id,
        language=language  # ✅ ADD HERE
    )



@app.route('/room_status/<room_id>')
def room_status(room_id):
    logger.debug(f"Accessing room_status for {room_id} with session: {session}")
    room = rooms.find_one({'_id': ObjectId(room_id)})
    if not room:
        logger.debug(f"Room {room_id} not found")
        return jsonify({'error': 'Room not found'}), 404
    # Allow students to check status, but only teachers get detailed info
    response = {'status': room.get('status', 'active')}
    if 'user_id' in session and session['role'] == 'teacher' and room['teacher_id'] == session['user_id']:
        response.update({
            'num_students': len(room.get('students', [])),
            'students': room.get('students', [])
        })
    return jsonify(response)

@app.route('/score/<room_id>')
def score(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to score {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    student_results = room.get('student_results', [])
    leaderboard = sorted(student_results, key=lambda x: x['score'], reverse=True)
    scores = [result['score'] for result in student_results]
    num_questions = room['num_questions']
    score_distribution = [0] * (num_questions + 1)
    for score in scores:
        score_distribution[score] += 1
    return render_template('score.html', room=room, leaderboard=leaderboard, score_distribution=score_distribution)

 

@app.route('/take_quiz/<quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    language = session.get('language', 'en')  # ✅ FIXED

    if 'user_id' not in session:
        logger.debug(f"Unauthorized access to take_quiz {quiz_id}: {session}")
        return redirect(url_for('login'))

    user_name = session['name']
    user_collection = db[user_name]
    quiz = user_collection.find_one({'_id': ObjectId(quiz_id)})

    if not quiz:
        return redirect(url_for('dashboard'))

    if 'current_question' not in session or 'quiz_id' not in session or session['quiz_id'] != quiz_id:
        session['current_question'] = 0
        session['quiz_id'] = quiz_id
        session['answers'] = {}

    current_question = session['current_question']

    if request.method == 'POST':
        user_answer = request.form.get(f'question_{current_question}')
        if user_answer:
            session['answers'][str(current_question)] = user_answer

        if 'next' in request.form and current_question < len(quiz['questions']) - 1:
            session['current_question'] = current_question + 1
            return redirect(url_for('take_quiz', quiz_id=quiz_id))

        elif 'submit_quiz' in request.form or current_question >= len(quiz['questions']) - 1:
            answers = session.get('answers', {})
            score = 0
            results = []

            for i, question in enumerate(quiz['questions']):
                user_answer = answers.get(str(i))
                correct = user_answer == question['correct_answer']
                if correct:
                    score += 1

                # Check if it's a translatable (NCERT) question
                q_text = question.get(f'question_{language}') or question.get('question')
                explanation_text = question.get(f'explanation_{language}') or question.get('explanation')

                results.append({
                    'question': q_text,
                    'user_answer': user_answer,
                    'correct_answer': question['correct_answer'],
                    'correct': correct,
                    'explanation': explanation_text
                })


            user_collection.update_one(
                {'_id': ObjectId(quiz_id)},
                {'$set': {'results': results, 'score': score, 'completed_at': datetime.datetime.now()}}
            )

            session.pop('current_question', None)
            session.pop('answers', None)
            session.pop('quiz_id', None)

            return render_template(
                'take_quiz.html',
                quiz=quiz,
                results=results,
                score=score,
                show_results=True,
                quiz_id=quiz_id,
                language=language  # ✅ PASS LANGUAGE TO TEMPLATE
            )

    return render_template(
        'take_quiz.html',
        quiz=quiz,
        current_question=current_question,
        quiz_id=quiz_id,
        language=language  # ✅ PASS LANGUAGE TO TEMPLATE
    )


@app.route('/download_results/<quiz_id>')
def download_results(quiz_id):
    if 'user_id' not in session:
        logger.debug(f"Unauthorized access to download_results {quiz_id}: {session}")
        return redirect(url_for('login'))
    user_name = session['name']
    user_collection = db[user_name]
    quiz = user_collection.find_one({'_id': ObjectId(quiz_id)})
    if not quiz or 'results' not in quiz:
        return "No results found", 404
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['Quiz Name', quiz.get('quiz_name', 'Unknown')])
    writer.writerow(['Score', f"{quiz.get('score', 0)}/{quiz.get('num_questions', 0)}"])
    writer.writerow(['Percentage', f"{(quiz.get('score', 0) / quiz.get('num_questions', 1) * 100):.2f}%"])
    writer.writerow([])
    writer.writerow(['Question Number', 'Question', 'Your Answer', 'Correct Answer', 'Result', 'Explanation'])
    for i, result in enumerate(quiz['results'], 1):
        writer.writerow([
            i,
            result['question'],
            result['user_answer'] or 'Not answered',
            result['correct_answer'],
            'Correct' if result['correct'] else 'Incorrect',
            result['explanation']
        ])
    content = output.getvalue()
    output.close()
    response = make_response(content)
    response.headers["Content-Disposition"] = f"attachment; filename=quiz_{quiz_id}_results.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route('/download_room_results/<room_id>')
def download_room_results(room_id):
    if 'user_id' not in session:
        logger.debug(f"Unauthorized access to download_room_results {room_id}: {session}")
        return redirect(url_for('login'))
    user_name = session['name']
    room = rooms.find_one({'_id': ObjectId(room_id)})
    if not room:
        return "Room not found", 404
    # Allow teachers to download all results, students only their own
    if session['role'] == 'student' and user_name not in room.get('students', []):
        logger.debug(f"Student {user_name} not authorized for room {room_id}")
        return "User not authorized for this room", 403
    student_result = None
    if session['role'] == 'student':
        student_result = next((result for result in room.get('student_results', []) if result['name'] == user_name), None)
    elif session['role'] == 'teacher' and room['teacher_id'] == session['user_id']:
        student_result = {'name': 'All', 'score': sum(r['score'] for r in room.get('student_results', [])), 'results': [r for r in room.get('student_results', []) for r in (r['results'] if 'results' in r else [])]}
    if not student_result or ('results' not in student_result and session['role'] == 'student'):
        logger.debug(f"No results found for {user_name} in room {room_id}")
        return "No results found for this user in the room", 404
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['Quiz Name', room.get('quiz_name', 'Unknown')])
    writer.writerow(['Score', f"{student_result.get('score', 0)}/{room.get('num_questions', 0)}"])
    writer.writerow(['Percentage', f"{(student_result.get('score', 0) / room.get('num_questions', 1) * 100):.2f}%"])
    writer.writerow([])
    writer.writerow(['Question Number', 'Question', 'Your Answer', 'Correct Answer', 'Result', 'Explanation'])
    if session['role'] == 'teacher':
        for i, result in enumerate(student_result['results'], 1):
            writer.writerow([
                i,
                result['question'],
                result['user_answer'] or 'Not answered',
                result['correct_answer'],
                'Correct' if result['correct'] else 'Incorrect',
                result['explanation']
            ])
    else:
        for i, result in enumerate(student_result['results'], 1):
            writer.writerow([
                i,
                result['question'],
                result['user_answer'] or 'Not answered',
                result['correct_answer'],
                'Correct' if result['correct'] else 'Incorrect',
                result['explanation']
            ])
    content = output.getvalue()
    output.close()
    response = make_response(content)
    filename = f"room_quiz_{room_id}_results_{'all' if session['role'] == 'teacher' else user_name}.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route('/logout')
def logout():
    logger.debug(f"Logging out with session: {session}")
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    session.pop('current_question', None)
    session.pop('answers', None)
    session.pop('quiz_id', None)
    session.pop('room_id', None)
    session.pop('questions', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
