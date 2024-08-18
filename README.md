
Multimodality RAG (MRAG): Extract, Store and Retrieve visual data from document


### Summary
If a RAG application (Retrieval Augmented Generation) is able to understand and extract information from wide variety of sources then its utility would be incrementally increased. RAG can extract information from different sources like image, graph, charts apart from traditional text document. This requires framework to understand and generate final response by coherently interpreting textual and visual information. 

### MRAG
Multimodality Retrieval Augment Generation. Enterprise data is usually stored in different folders. These folders contain files that are of different modality. Text and Image modality are commonly found. RAG application should be able to extract and understand information stored in different modality documents. Multimodality files are unstructured and usually have format different from each other. Multimodality files makes RAG pipeline complex because different approach and method would be used to extract information.

### Chanllenges with documents that contains image
Normally we use embedding models to convert textual data into vectors. These textual embeddings models only convert textual data and not suitable for images. There are various other embedding models available to convert images into vector. We need to utilize both embedding models if we want to convert textual document that contains images or diagrams.
 <Diagram_1>

Similar to above, document and report may contain information-dense images like charts and diagrams. These elements have additional context and many points of interest. RAG pipeline must effectively capture these visual elements along with textual data. You must make sure semantic representation of charts and diagrams aligns with semantic meaning of text.

### Approach for Multimodal RAG
With key challenges understood, Let's discuss architecture to tackle these challenges. One approach to solve this problem is to ground all modalities (text, image, charts) to one primary modality and encode that modality into vector space. In this case, **Processing Phase**: process text normally but for images, first create text description, summary or metadata in processing step. Actual image is also stored for later retrieval. **Retrieval Phase**: retrieval part primarily extracts text chunks and image metadata. Final answer is generated with LLMs along with image (chart) that ground the generated response.

### Visual Language Model (VLM)
Large Language Models (LLMs) are designed to understand, interpret, and generate text-based information. LLMs are trained on vast amounts of textual data, LLMs can perform a range of natural language processing tasks, such as text generation, summarization, question-answering, and more.

Visual Language Models (VLMs) takes both images and text as inputs and can answer questions about images with detail and context, VLMs can perform deeper analysis of images and provide useful insights, such as captioning for images, object detection, and reading text embedded within images.

In this example following models and tools are used to build RAG pipeline:
**LLM**: OpenAI, Claude, Llama 3 for general reasoning and question answering.
**VLM**: Microsoft Kosmos 2, Paligemma for visual question answering and image description.
**DePlot**: Subset of VLM to comprehend charts and plots
**Embedding model**: Encoding data into vectors
**Vector database**: Storing and retrieval of vectors


### Extracting multimodal data and creating a vector database
The first step for building a RAG pipeline is to preprocess your data and store it as vectors in a vector store so that you can then retrieve relevant vectors based on a query. With images present in the data, here is a generic RAG preprocessing workflow to work through (Figure 2).

// Figure 2: Simple LLM flow.

The document may contains several images, bar charts like Figure 3 or textual data. To interpret these bar charts, use Google’s DePlot, a visual-language model capable of comprehending charts and plots when coupled with an LLM.

// Figure 3: Demonstration of Google's DePlot

Document can have other images . Paligemma VLM is capable of performing various tasks like: comprehending, extracting objects, answer questions and extracting deeper information about images. Paligemma generally works for most types of images but if you want to use it for specific precision use case like medical, construction images etc. consider to fine tune it.

// Figure 4: Demonstration of Google's Paligemma

With knowledge of working of Paligemma and DePlot, Let's expand the preprocessing pipeline that we discuss in Figure 2 to dive deeper into handling each modality in the pipeline that leverages textual data extractors, VLM and LLM to create vectors.

// Figure 5: In depth RAG Pipeline.

### MRAG workflow
The goal is to ground images to text modality. Start by extracting and classifying your data into images and text. Then handle these two modalities separately to eventually store them into vector store.

Paligemma VLM can generate image description and can be used to classify images into categories whether they are graphs or not. Based on classification, use DePlot to convert graphs and charts to linearized tabular text. Since this tabular text is different from regular text, this text is summarized using LLM so that it can be retrieved from vector store easily in subsequent retrieval phase. Similarly normal images context is captured in description and that is also stored in vector storage.
Regular text is extracted from document using traditional OCR, Extracted text is chunked (using chunking strategy ## Include the Link) and vectors are stored in vector storage.

### Talking to your application
Following above steps, you have captured all the multimodal information present in the PDF. Here's how RAG pipeline will work when user asks a question.
When a user asks the system with a question, MRAG pipeline converts question into an embedding and performs semantic search to retrieve relevant chunks from store. Since these chunks are also retrieved from images or chart descriptions, you need to take additional steps before sending these chunks to LLM for final response.

// Figure 6: How user tackle user query by retrieving relevant information from both image and text.

Here are further steps that MRAG pipeline takes after retrieving relevant chunks from the vector store:
1. If chunk is retrieved from the description generated by Paligemma then stored image is simply send along with user's question to Paligemma (VLM) to generate the answer. This is nothing but VQA task. VLM is capable to understand image semantics and objects inside the image. Generated answer is sent as context to LLM
2. If chunk is retrieved from chart or plot, then linearized table data stored as summarized text is appended as context.
3. The chunk coming from regular text are used as it is.

All these chunks, along with the user question, are now ready to generate a final answer. From document in #Fig: 1 LLM referred images and text generated the final response.


// Figure 7: Actual response




TITLE |  <0x0A>  |  <0x0A> Beneficiary<0x0A>Registered<0x0A>Registered <0x0A> Site Geo<0x0A>Tagged | 86 <0x0A> House<0x0A>Sanctioned | 136 <0x0A> House<0x0A>Completed | 108




Entity      | Individuals responsibility  | Government's responsibility 
MEDIAN      | 39.0                        | 55.0
Germany     | 57.0                        | 35.0
UK          | 45.0                        | 49.0
Sweden      | 37.0                        | 53.0
Denmark     | 42.0                        | 54.0
France      | 38.0                        | 55.0
Netherlands | 40.0                        | 58.0
Spain       | 29.0                        | 63.0
Italy       | 22.0                        | 74.0





DePlot: Plot-to-text translation

Vision and Vision Language task.
Caption, Object detection, Segmentation

- Read images from folder.
- Pass them to model to extract information.
- Save the data to file.
- So that I can plot and view it later on.
- OCR doesn't work

- Extract Image and its description
