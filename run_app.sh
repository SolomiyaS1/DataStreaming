#!/bin/bash
cd Services
python sentimment_detector.py &
python language_detector.py &
python entity_detector.py &
python statistic_generator_1.py &
python statistic_generator_2.py &
python generator.py