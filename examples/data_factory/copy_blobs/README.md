# Copy Blobs

This is an example pipeline which intends to list all the blobs in a given container and copies these blobs to another container

<image src="copy_blobs.png"></img>

The pipeline has two activities:

1. **List folders**: Web activity to list all blobs in a container that has a given prefix
2. **For each activity**: Iterates over each item in the list returned above and executes the sub-activity on each item.

    2.1. **Copy files to destination**: Copy activity which copies the blobs to a given destination.
