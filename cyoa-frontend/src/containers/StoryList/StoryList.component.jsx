import React from 'react'

const StoryList = ({ data }) => {
  
  return (
    <div>
        A list of Stories.
        { !data.loading && !data.error && data.storyConnection.edges.map(({ node }) => {
          return <div key={node.id}>{node.title} - {node.author}</div>
        }) }
    </div>
  )
}

export default StoryList