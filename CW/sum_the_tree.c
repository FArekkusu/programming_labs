#include <stddef.h>
#include <stdio.h>

struct node
{
  int value;
  struct node* left;
  struct node* right;
};


int sumTheTreeValues(struct node* root)
{
  int left = (root->left != NULL)?sumTheTreeValues(root->left):0;
  int right = (root->right != NULL)?sumTheTreeValues(root->right):0;
  return root->value + left + right;
}
