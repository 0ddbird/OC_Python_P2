# Project : a naive homemade parser

Given a well structured HTML content:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div id="parent_div_one">
        <div class="sub">Sub div 1</div>
        <div class="sub">Sub div 2</div>
    </div>
</body>
</html>
```

The parser could read the html content as a string and store it's content as a tree
```python
dom = [
    (
        '!DOCTYPE',
        {
            'attrs': (('html', True),),
            'inner_text': None,
            'children': None
        }
    ),
    (
        'html', 
        {
            'attrs': None,
            'inner_text': None,
            'children': 
            (
                (
                    'head',
                    {
                        'attrs': None,
                        'inner_text': None,
                        'children':
                            (
                                (
                                    'meta',
                                        {
                                            'attrs': (('charset', 'UTF-8'),),
                                            'inner_text': None,
                                            'children': None,
                                        }
                                ),
                                (
                                    'title',
                                    {
                                        'attrs': None,
                                        'inner_text': 'Title',
                                        'children': None
                                    }
                                )
                            )
                        }
                ),
                (
                    'body',
                    {
                        'attrs': None,
                        'inner_text': None,
                        'children': 
                            (
                                (
                                    'div',
                                    {
                                        'attrs': (('id', 'parent_div_one'),),
                                        'inner_text': None,
                                        'children': 
                                            (
                                                (
                                                    'div',
                                                    {
                                                        'attrs': (('class', 'sub'),),
                                                        'inner_text': 'Sub div 1',
                                                        'children': None
                                                    }
                                                ),
                                                (
                                                    'div',
                                                    {
                                                        'attrs': (('class', 'sub'),),
                                                        'inner_text': 'Sub div 2',
                                                        'children': None
                                                    }
                                                )
                                            )
                                    }

                                )
                            )
                    }
                )
            )
            
        }
    )
]
```

A functional but rough way to access an element of the tree:

```python
html_element_children = dom[1][1]['children']
```

However, during the creation of the tree, it's possible to store a more direct reference to elements using their attributes, enabling a search similar to a querySelector:

```python
dom_attrs = {
    'class': {
        'sub': (
            (
                'div',
                {
                    'attrs': (('class', 'sub'),),
                    'inner_text': 'Sub div 1',
                    'children': None
                }
            ),
            (
                'div',
                {
                    'attrs': (('class', 'sub'),),
                    'inner_text': 'Sub div 2',
                    'children': None
                }
            )
        )
    }
}
sub_class_elements = dom_attrs['class']['sub']
```
Another way to structure the tree could also enable the search by tag:

```python

new_dom = (
    {
        'tag': 'div',
        'attrs': (('id', 'parent_div_one'),),
        'inner_text': None,
        'children': 
            (
                {
                    'tag': 'div',
                    'attrs': (('class', 'sub'),),
                    'inner_text': 'Sub div 1',
                    'children': None
                },
                {
                    'tag': 'div',
                    'attrs': (('class', 'sub'),),
                    'inner_text': 'Sub div 2',
                    'children': None
                }
            )
    }
)
```

This way it would be possible to create 3 structures during parsing: a dom-like tree, a tags dictionary and an attribute dictionary

A set of unique tags:
```python
elements_by_tag = {
    'html': [html_ref],
    'head': [head_ref],
    'meta': [meta_ref],
    'title': [title_ref],
    'body': [body_ref],
    'div': 
        [
            div1_ref, 
            div2_ref, 
            div3_ref
        ],
}
```


