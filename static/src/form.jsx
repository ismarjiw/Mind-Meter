var data;
function WriteReflection() {
    const [title, setTitle] = React.useState('');
    const [content, setContent] = React.useState('');
    const [tag, setTag] = React.useState('');

    function handleSubmit(event) {
      event.preventDefault();

      const title = document.querySelector('#title').value;
      const content = document.querySelector('#content').value;
      const tag = document.querySelector('#tag').value;

      fetch('/reflection', {
        method: 'POST',
        body: JSON.stringify({title, content, tag}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
      if (responseJson.status == 'Meditate again first') {
        swal("Oh Noes!", responseJson.status, "error");
      } else if (responseJson.status == 'Your reflection is saved 😌') {
        swal ("Aww yiss!", responseJson.status, "success")
      }
      data = responseJson['reflection_id'];
    });
    setTitle('');
    setContent('');
    setTag('');
    };

    return (
      <form onSubmit={handleSubmit}>
        <div className="notes__preview">
          <input id="title" className="notes__title" type="text" placeholder="Enter a title..." name="title" onChange={event => setTitle(event.target.value)} value={title} />
          <textarea id="content" className="notes__body" placeholder="Enter your message..." name="content" onChange={event => setContent(event.target.value)} value={content} ></textarea>
          <input id="tag" className="notes__tag" type="text" placeholder="Enter a tag..." name="tag" onChange={event => setTag(event.target.value)} value={tag}  />
        </div>
        <button type="submit" className="text-white bg-gradient-to-br from-green-400 to-blue-600 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-green-200 dark:focus:ring-green-800 font-medium rounded-lg text-md px-5 py-2.5 text-center mr-2 mb-2">Add Reflection</button>
        <button onClick="location.href='/journal'" type="button" className="text-white bg-gradient-to-br from-purple-400 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2">Reflection Entries</button>
      </form>
    );
  };
  
  ReactDOM.render(<WriteReflection />, document.querySelector('#root'));