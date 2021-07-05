#!/bin/bash
cd Services
python generator.py &
python language_detector.py &
python sentimment_detector.py &
python entity_detector.py &
python statistic_generator_1.py &
python statistic_generator_2.py &