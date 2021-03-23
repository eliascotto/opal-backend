import os
import ast
import subprocess
from typing import List, Dict, Optional
from pydantic import BaseModel, constr


block_keys = [
    "type",
    "position",
    "indent",
    "list",
    "properties",
    "children"
]


class Block(BaseModel):
    """
    Class rapresenting the block as stored into the db
    """
    type: constr(max_length=16)
    position: Optional[int]
    indent: Optional[int] = 0
    list: Optional[constr(max_length=1)]
    properties: Optional[Dict]
    content: Optional[List[Dict]]

    def to_dict(self):
        """
        convert Block objects to dict for using with schemas.BlockCreate
        """
        return {
            "type": self.type,
            "position": self.position,
            "indent": self.indent,
            "list": self.list,
            "properties": self.properties,
            "content": self.content,
        }


def webpage2blocks(url):
    process = subprocess.Popen(
        ["node", os.path.abspath("web2markdown/dist/index.js"), url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    out, err = process.communicate()

    if err:
        print(err)
        raise Exception("Impossible to retrieve article {}".format(url))

    out_str = out.decode().strip()

    cleaned_str = (
        out_str
        .replace("null", "None")
        .replace("true", "True")
        .replace("false", "False")
    )

    try:
        info = ast.literal_eval(cleaned_str)
    except:
        raise Exception("Error evaluating article")

    blocks = []

    for blk in info["blocks"]:
        props = blk["properties"]
        # Add other properties
        for key, value in blk.items():
            if key not in block_keys:
                props[key] = value

        if "children" in blk:
            content = blk["children"]
        else:
            content = [{ "value": blk["value"], "type": blk["type"] }]
        
        block = Block(
            type=blk["type"],
            position=blk["position"],
            indent=blk["indent"],
            list=blk["list"],
            content=content,
            properties=props
        )

        blocks.append(block)

    return { "raw": info["raw"], "blocks": blocks, "meta": info["meta"] }


if __name__ == "__main__":
    test_page = "http://www.paulgraham.com/start.html"

    # external = webpage2blocks("https://typemill.net/info/markdown-test")
    external = webpage2blocks("http://www.aaronsw.com/weblog/productivity")

    for blk in external["blocks"]:
        print(blk.to_dict())
        