# Language Intelligence Model Evaluation (LIME)



## Overview
- [Introduction ℹ](#introduction)
- [Installation guide 🦮](#installation-guide)
- [How to use it 🤔?](#how-to-use-it)

<h2 id="introduction">Introduction ℹ</h2>
Specialized LLMs are designed for a broad array of tasks across domains. Datasets like MMLU, ARC, HellaSwag, and TruthfulQA are used to evaluate and benchmark models across these generalized tasks and domains.  
These are standardized benchmarks that provide valuable insights into the generalized quality of the output of the models. They are also widely used to score, compare, and rank the models like the popular hugging face leaderboard.   
These evaluation techniques use a binary scoring methodology, where the answer is precisely equal to the ground truth.  Given the nature of LLMs for a given input, expecting the same output every time is uncertain.  For example, a model trained in medical information provides a brief description of the ailment based on a patient’s medical history. In such scenarios, a binary score does not provide an accurate evaluation of the quality of the model’s response. This calls for a different approach to evaluating specialized models which gives a deeper understanding of the model’s performance.
LLMs are now fine-tuned for domain-specific task use cases like patient interaction in health,  contract review in law, and company analysis in finance. These evaluation techniques do not address the evaluation of specialized models that are exclusively trained for a particular subject matter. 
For example, the Massive Multitask Language Understanding (MMLU) evaluation technique measures the knowledge acquired by models during pretraining and evaluates their performance in zero-shot and few-shot settings across 57 subjects like mathematics, history, and law. A fine-tuned model that is trained specifically for patient interactions in healthcare will not be able to score high on the MMLU evaluation. 
In the context of evaluating such models trained for domain-specific tasks, we introduce the Language Intelligence Model Evaluation (LIME) framework to quickly test multiple models against specific tasks and domains. 

<h2 id="installation-guide">Installation guide 🦮</h2>

- Install [Python](https://www.python.org) or [Anaconda](https://www.anaconda.com) your system.  
- Open up your terminal and clone this repository using the below command:

 ```sh
   git clone https://github.com/IceCream-Labs/Lime
 ```
- Create a virtual environment and install the dependencies mentioned in requirements.txt
 ```sh
   pip install -r requirements.txt
 ```
- Now, check out [How to use it 🤔?](#how-to-use-it) section to know how to run the application

<h2 id="how-to-use-it">How to use it 🤔?</h2>

- Once you have done with all the steps mentioned in [Installation guide 🦮](#installation-guide) you are good to go.
- Check out [this notebook](https://github.com/IceCream-Labs/Lime/blob/main/Test/runTest.ipynb), it contains all the commands that you can perform for evaluation.

<h2>License </h2>

Copyright (C)2023 IceCreamlabs Inc

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.  You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

If your software can interact with users remotely through a computer network, you should also make sure that it provides a way for users to get its source. 

For example, if your program is a web application, its interface could display a "Source" link that leads users to an archive of the code. There are many ways you could offer source, and different solutions will be better for different programs; see section 13 for the specific requirements.
