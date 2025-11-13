def safe_fallback(function,**kwargs):
    """Execute a function with asynchronous fallback for exceptions.

    Args:
        function (callable): The asynchronous function to execute.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        result: The result of the function execution, or a fallback error message if an exception occurs.
    """
    try:
        return function(**kwargs)
    except Exception as e:
        state = kwargs['state']
        state['response']="LLM Failed due to overload please try again later."
        return state