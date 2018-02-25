import gql from 'graphql-tag'
import { graphql } from 'react-apollo'

import StoryList from './StoryList.component'

const storyListForLayout = gql`
{
    storyConnection(first: 5) {
        totalStories
        edges {
            node {
                id
                title
                author
                createdAt
                updatedAt
                datePublished
                passageConnection(first: 1) {
                    edges {
                        node {
                            id
                            name
                            description
                        }
                    }
                }
            }
        }
    }
}
`;


const withStoryListQuery = graphql(storyListForLayout)

export default withStoryListQuery(StoryList)