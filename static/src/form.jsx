var data;
function WriteReflection() {
    const ref = React.useRef();
    
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
      data = responseJson['reflection_id'];
    });
    };

    function reset(event) {
      event.preventDefault();
      ref.current.reset();
    };

    return (
      <form ref={ref} onSubmit={handleSubmit}>
        <div className="notes__preview">
          <input id="title" className="notes__title" type="text" placeholder="Enter a title..." name="title" />
          <textarea id="content" className="notes__body" placeholder="Enter your message..." name="content"></textarea>
          <input id="tag" className="notes__tag" type="text" placeholder="Enter a tag..." name="tag" />
        </div>
        <button type="submit" className="text-white bg-gradient-to-br from-green-400 to-blue-600 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-green-200 dark:focus:ring-green-800 font-medium rounded-lg text-md px-5 py-2.5 text-center mr-2 mb-2">Add Reflection</button>
        <button onclick={reset} className="text-white bg-gradient-to-br from-green-400 to-blue-600 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-green-200 dark:focus:ring-green-800 font-medium rounded-lg text-md px-5 py-2.5 text-center mr-2 mb-2">Reset</button>
      </form>
    );
  }
  
  ReactDOM.render(<WriteReflection />, document.querySelector('#root'));